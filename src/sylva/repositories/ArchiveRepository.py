from pymongo import MongoClient
from pymongo.collection import Collection
import os
from sylva.MetaData import MetaData

from sylva.Configuration import DatabaseConfig, Folder
from sylva.Configuration import Configuration

class ArchiveRepository():
    client = None
    __folder_configuration = None

    def __init__(self, configuration: Configuration) -> None:
        database_configuration = configuration.get_database_config()
        self.__folder_configuration = configuration.get_folders()

        self.client = MongoClient(
            database_configuration[DatabaseConfig.HOST.value], 
            port=database_configuration[DatabaseConfig.PORT.value],
            username = database_configuration[DatabaseConfig.USER.value],
            password = database_configuration[DatabaseConfig.PASSWORD.value],
            authSource = "admin"
        )


    def __get_archive_collection(self) -> Collection:
        return self.client.sylva.archive
    
    def has(self, meta_data: MetaData) -> bool:
        return self.__get_archive_collection().find_one(meta_data.get_key_fields())
    
    def add(self, meta_data: MetaData):
        return self.__get_archive_collection().insert_one(meta_data)
    
    def get_archive_path(self, meta_data: MetaData):
        return os.path.join(self.__folder_configuration[Folder.ARCHIVE.value], meta_data["deviceLocation"], meta_data["start"].strftime("%Y"), meta_data["start"].strftime("%m"))

