import hashlib

class Device:
    HASH_ALGORITHM = "sha256"
    file = None

    def __init__(self, file) -> None:
        self.file = file

    def get_file_hash(self) -> str:
        hash_algorithm = hashlib.new(self.HASH_ALGORITHM)

        with open(self.file, 'rb') as file:
            for chunk in iter(lambda: file.read(4096), b''):
                hash_algorithm.update(chunk)

        return hash_algorithm.hexdigest()