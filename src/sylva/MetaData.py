from datetime import datetime, timezone


class MetaData(dict):
    @staticmethod
    def from_dict(input):
        return MetaData(
            start=input["start"],
            end=input["end"],
            deviceLocation=input["deviceLocation"],
            device_type=input["deviceType"],
            file_path=input["filePath"],
            file_name=input["fileName"],
            file_hash=input["fileHash"],
            is_archived=input["isArchived"],
            created_on=input["createdOn"],
            archive_on=input["archivedOn"],
        )

    def __init__(self, start: datetime, end: datetime, deviceLocation: str, file_name: str, file_hash: str, device_type: str, is_archived: bool = False, created_on: datetime = datetime.now(timezone.utc), archive_on: datetime = None, file_path: str = None):
        super().__init__()
        self["start"] = start
        self["end"] = end
        self["deviceLocation"] = deviceLocation
        self["deviceType"] = device_type
        self["filePath"] = file_path
        self["fileName"] = file_name
        self["fileHash"] = file_hash
        self["isArchived"] = is_archived
        self["createdOn"] = created_on
        self["archivedOn"] = archive_on

    def set_file_path(self, path) -> None:
        self["filePath"] = path

    def get_key_fields_array(self):
        return [{"start": self.get("start")}, {"end": self.get("end")}, {"deviceLocation": self.get("deviceLocation")}, {"fileHash": self.get("fileHash")}, {"deviceType": self.get("deviceType")}]

    def get_start(self) -> datetime:
        return self.get("start")

    def get_end(self) -> datetime:
        return self.get("end")

    def get_device_location(self) -> str:
        return self.get("deviceLocation")

    def get_file_path(self) -> str:
        return self.get("filePath")

    def get_file_name(self) -> str:
        return self.get("fileName")

    def get_file_hash(self) -> str:
        return self.get("fileHash")

    def get_device_type(self) -> str:
        return self.get("deviceType")

    def get_is_archived(self) -> bool:
        return self.get("isArchived")
