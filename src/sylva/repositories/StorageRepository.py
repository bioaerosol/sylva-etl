import shutil
import os
import uuid
from sylva.MetaData import MetaData

from sylva.Configuration import Configuration
from sylva.repositories.DatabaseRepository import DatabaseRepository

class StorageRepository(DatabaseRepository):
    client = None
    storage_base_path = None
    trash_base_path = None

    def __init__(self, configuration: Configuration, storage_base_path: str, trash_base_path: str) -> None:
        super().__init__(configuration)
        self.storage_base_path = storage_base_path
        self.trash_base_path = trash_base_path
    
    def has(self, meta_data: MetaData) -> bool:
        return self.get_storage_collection().find_one({ "$and": meta_data.get_key_fields_array() }) is not None
    
    def store(self, source_file: str, meta_data: MetaData) -> str:
        # determine target
        storage_target_path = self.__get_storage_path(meta_data)
        storage_target_file = os.path.join(storage_target_path, os.path.basename(source_file))

        # update meta_data with target
        meta_data.set_file_path(storage_target_path)
        
        # file system operations
        os.makedirs(storage_target_path, exist_ok=True)
        shutil.move(source_file, storage_target_file)

        # put meta_data to index
        self.get_storage_collection().insert_one(meta_data)

        return storage_target_file

    def trash(self, source_file: str, process_id: str) -> str:
        # determine target
        trash_target_path = os.path.join(self.trash_base_path, process_id)
        trash_target_file = os.path.join(trash_target_path, str(uuid.uuid4()) + "-" + os.path.basename(source_file))
    
        # file system operations
        os.makedirs(trash_target_path, exist_ok=True)
        shutil.move(source_file, trash_target_file)

        return trash_target_file
    
    def __get_storage_path(self, meta_data: MetaData):
        return os.path.join(self.storage_base_path, meta_data["deviceLocation"], meta_data.get_device_type(), meta_data.get_start().strftime("%Y"), meta_data.get_start().strftime("%m"), meta_data.get_start().strftime("%d"))

