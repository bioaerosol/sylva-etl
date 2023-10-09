
class MetaData(dict):
    def __init__(self, start: int, end: int, file_hash: str):
        super().__init__()
        self["start"] = start
        self["end"] = end
        self["fileHash"] = file_hash
