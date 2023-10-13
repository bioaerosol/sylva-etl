from sylva.devices.Device import Device
from sylva.MetaData import MetaData

from dateutil.parser import parse
from dateutil import tz

import zipfile
import re
import os
import xml.etree.ElementTree as ElementTree


class BAA500(Device):
    """Actual implementation for Hund monitor BAA500."""

    VENDOR = "Hund GmbH"
    BAA500_TIME_ZONE = "Europe/Berlin"
    CONTENT_XML_FILE_PATTERN = re.compile(r".*\/analysis\/polle.*\.xml")

    @staticmethod
    def timestamp_to_unix_epoch(timestamp: str):
        """Returns a given timestamp string from BAA500 XML file as unix epoch (seconds). Timestamp is interpreted
        in time zone Europe/Berlin, seconds are set to 0 in general as BAA500 reports for whole minutes."""
        ts = parse(timestamp)
        if ts.time().minute <= 10:
            ts = ts.replace(minute=0)

        return int(ts.replace(second=0).replace(tzinfo=tz.gettz(BAA500.BAA500_TIME_ZONE)).timestamp())

    def get_data_file_meta_data(self) -> MetaData:
        if self.__isMine():
            with zipfile.ZipFile(self.file, "r") as data_file:
                xml_filename = [entry for entry in data_file.namelist() if self.CONTENT_XML_FILE_PATTERN.search(entry)][0]
                with data_file.open(xml_filename) as xml_file:
                    # Lies den Inhalt der Datei
                    file_content = xml_file.read()
                    xml_root = ElementTree.fromstring(file_content)
                    start = xml_root.find("./Beginn_der_Probenahme")
                    end = xml_root.find("./Ende_der_Probenahme")

            return MetaData(BAA500.timestamp_to_unix_epoch(start.text), BAA500.timestamp_to_unix_epoch(end.text), super().get_file_hash())
        else:
            return None

    def __isMine(self) -> bool:
        if not os.path.isfile(self.file):
            return False

        if not os.access(self.file, os.R_OK):
            return False

        try:
            with zipfile.ZipFile(self.file, "r") as data_file:
                matching_entries = [entry for entry in data_file.namelist() if self.CONTENT_XML_FILE_PATTERN.search(entry)]
                return len(matching_entries) > 0
        except:
            return False
