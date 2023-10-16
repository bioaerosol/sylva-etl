from datetime import datetime

class MetaData(dict):
    def __init__(self, start: datetime, end: datetime, deviceLocation: str, filename: str, file_hash: str, device_type: str):
        super().__init__()
        self["start"] = start
        self["end"] = end
        self["deviceLocation"] = deviceLocation
        self["fileName"] = filename
        self["fileHash"] = file_hash
        self["deviceType"] = device_type

    def set_archive_path(self, path) -> None:
        self["path"] = path

    def get_key_fields_array(self):
        return [
            { "start": self.get("start") },
            { "end": self.get("end") },
            { "deviceLocation": self.get("deviceLocation") },
            { "fileHash": self.get("fileHash") },
            { "deviceType": self.get("deviceType") }
        ]
    
    def get_start(self) -> datetime:
        return self.get("start")

    def get_end(self) -> datetime:
        return self.get("end")

    def get_device_location(self) -> str:
        return self.get("deviceLocation")

    def get_filename(self) -> str:
        return self.get("fileName")

    def get_path(self) -> str:
        return self.get("path")

    def get_file_hash(self) -> str:
        return self.get("fileHash")

    def get_device_type(self) -> str:
        return self.get("deviceType")