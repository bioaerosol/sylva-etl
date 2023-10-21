from sylva.MetaData import MetaData
from sylva.repositories import DevicesRepository

import hashlib

from abc import abstractmethod
from enum import Enum

class DeviceType(Enum):
    Poleno = "Poleno"
    BAA500 = "BAA500"
    RapidE = "Rapid-E+"

class Device:
    HASH_ALGORITHM = "sha256"
    file = None

    def __init__(self, file, devices_repository: DevicesRepository) -> None:
        self.file = file
        self.devices_repository = devices_repository

    def get_file_hash(self) -> str:
        hash_algorithm = hashlib.new(self.HASH_ALGORITHM)

        with open(self.file, "rb") as file:
            for chunk in iter(lambda: file.read(4096), b""):
                hash_algorithm.update(chunk)

        return hash_algorithm.hexdigest()

    def get_location(self, device_id : str) -> str:
        return self.devices_repository.get_location_for(self.get_device_type(), device_id)

    @abstractmethod
    def get_data_file_meta_data(self) -> MetaData:
        return NotImplemented
    
    @abstractmethod
    def get_device_type(self) -> str:
        return NotImplemented