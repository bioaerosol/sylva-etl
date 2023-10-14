
class MetaData(dict):
    def __init__(self, start: int, end: int, deviceLocation: str, filename: str, path: str, file_hash: str):
        super().__init__()
        self["start"] = start
        self["end"] = end
        self["deviceLocation"] = deviceLocation
        self["fileName"] = filename
        self["path"] = path
        self["fileHash"] = file_hash
