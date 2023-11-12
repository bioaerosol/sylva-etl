from sylva.devices.Device import Device, DeviceType
from sylva.MetaData import MetaData

from datetime import datetime, timezone

import re
import os
import zipfile
import json


class Poleno(Device):
    """Actual implementation for Swisens Poleno."""

    DEVICE_TYPE = DeviceType.Poleno.value
    CONTENT_JSON_FILE_PATTERN = re.compile(r".*\/.*_.*_ev\.json")
    POLENO_TIME_ZONE = "Europe/Berlin"

    @staticmethod
    def timestamp_to_datetime(timestamp: str):
        """Returns a given timestamp string from Poleno JSON event file as unix epoch (seconds). Timestamp is interpreted
        in time zone UTC, milliseconds are set to 0 in general purpose of this is indexing only."""
        return datetime.strptime(timestamp, "%Y-%m-%d_%H.%M.%S.%f").replace(microsecond=0).replace(tzinfo=timezone.utc)

    def get_data_file_meta_data(self) -> MetaData:
        if self.__isMine():
            device_id = None

            with zipfile.ZipFile(self.file, "r") as data_file:
                event_file_filenames = [entry for entry in data_file.namelist() if self.CONTENT_JSON_FILE_PATTERN.search(entry)]
                timestamps = []
                for event_file_filename in event_file_filenames:
                    with data_file.open(event_file_filename) as event_file:
                        data = json.load(event_file)
                        timestamps.append(Poleno.timestamp_to_datetime(data["timestamp_dt"]))
                        device_id = data["metadata"]["poleno_id"] if device_id == None else device_id 

            timestamps.sort()

            return MetaData(
                start=timestamps[0], 
                end=timestamps[len(timestamps) - 1], 
                file_hash=super().get_file_hash(),
                file_name=os.path.basename(self.file),
                device_type=self.get_device_type(),
                deviceLocation=self.get_location(device_id),
                file_size=os.path.getsize(self.file),
                is_in_storage=True
            )
        
        else:
            return None

    def get_device_type(self) -> str:
        return Poleno.DEVICE_TYPE

    def __isMine(self) -> bool:
        if not os.path.isfile(self.file):
            return False

        if not os.access(self.file, os.R_OK):
            return False

        try:
            with zipfile.ZipFile(self.file, "r") as data_file:
                matching_entries = [entry for entry in data_file.namelist() if self.CONTENT_JSON_FILE_PATTERN.search(entry)]
                return len(matching_entries) > 0
        except:
            return False
