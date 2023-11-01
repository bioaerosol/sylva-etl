from pymongo import MongoClient
from pymongo.collection import Collection
import shutil
import os
import uuid
from sylva.MetaData import MetaData

from sylva.Configuration import DatabaseConfig, Folder
from sylva.Configuration import Configuration

class DataRepository():
    client = None
    archive_base_path = None
    trash_base_path = None

    def __init__(self, configuration: Configuration, archive_base_path: str, trash_base_path: str) -> None:
        self.archive_base_path = archive_base_path
        self.trash_base_path = trash_base_path

        database_configuration = configuration.get_database_config()
        
        self.client = MongoClient(
            database_configuration[DatabaseConfig.HOST.value], 
            port=database_configuration[DatabaseConfig.PORT.value],
            username = database_configuration[DatabaseConfig.USER.value],
            password = database_configuration[DatabaseConfig.PASSWORD.value],
            authSource = "admin"
        )


    def __get_archive_collection(self) -> Collection:
        return self.client.sylva.data
    
    def has(self, meta_data: MetaData) -> bool:
        return self.__get_archive_collection().find_one({ "$and": meta_data.get_key_fields_array() }) is not None
    
    def archive(self, source_file: str, meta_data: MetaData) -> str:
        # determine target
        archive_target_path = self.__get_archive_path(meta_data)
        archive_target_file = os.path.join(archive_target_path, os.path.basename(source_file))

        # update meta_data with target
        meta_data.set_file_path(archive_target_path)
        
        # file system operations
        os.makedirs(archive_target_path, exist_ok=True)
        shutil.move(source_file, archive_target_file)

        # put meta_data to index
        self.__get_archive_collection().insert_one(meta_data)

        return archive_target_file

    def trash(self, source_file: str, process_id: str) -> str:
        # determine target
        trash_target_path = os.path.join(self.trash_base_path, process_id)
        trash_target_file = os.path.join(trash_target_path, str(uuid.uuid4()) + "-" + os.path.basename(source_file))
    
        # file system operations
        os.makedirs(trash_target_path, exist_ok=True)
        shutil.move(source_file, trash_target_file)

        return trash_target_file
    
    def __get_archive_path(self, meta_data: MetaData):
        return os.path.join(self.archive_base_path, meta_data["deviceLocation"], meta_data.get_device_type(), meta_data.get_start().strftime("%Y"), meta_data.get_start().strftime("%m"), meta_data.get_start().strftime("%d"))

