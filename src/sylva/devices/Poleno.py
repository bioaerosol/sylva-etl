from sylva.devices.Device import Device
from sylva.MetaData import MetaData

from dateutil.parser import parse
from dateutil import tz

from datetime import datetime

import re
import os
import zipfile
import json


class Poleno(Device):
    """Actual implementation for Swisens Poleno."""

    VENDOR = "Swisens"
    CONTENT_JSON_FILE_PATTERN = re.compile(r".*\/.*_.*_ev\.json")
    POLENO_TIME_ZONE = "Europe/Berlin"

    @staticmethod
    def timestamp_to_unix_epoch(timestamp: str):
        """Returns a given timestamp string from Poleno JSON event file as unix epoch (seconds). Timestamp is interpreted
        in time zone Europe/Berlin, milliseconds are set to 0 in general purpose of this is indexing only."""
        return int(datetime.strptime(timestamp, "%Y-%m-%d_%H.%M.%S.%f").replace(microsecond=0).replace(tzinfo=tz.gettz("Europe/Berlin")).timestamp())

    def get_data_file_meta_data(self) -> MetaData:
        if self.__isMine():
            with zipfile.ZipFile(self.file, "r") as data_file:
                event_file_filenames = [entry for entry in data_file.namelist() if self.CONTENT_JSON_FILE_PATTERN.search(entry)]
                timestamps = []
                for event_file_filename in event_file_filenames:
                    with data_file.open(event_file_filename) as event_file:
                        data = json.load(event_file)
                        timestamps.append(Poleno.timestamp_to_unix_epoch(data["timestamp_dt"]))

            timestamps.sort()
            return MetaData(timestamps[0], timestamps[len(timestamps) - 1], super().get_file_hash())
        else:
            return None

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
