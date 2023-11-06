from pymongo import MongoClient
from pymongo.collection import Collection

from sylva.Configuration import DatabaseConfig
from sylva.Configuration import Configuration

class DatabaseRepository():
    client = None

    def __init__(self, configuration: Configuration) -> None:
        database_configuration = configuration.get_database_config()
        
        self.client = MongoClient(
            database_configuration[DatabaseConfig.HOST.value], 
            port=database_configuration[DatabaseConfig.PORT.value],
            username = database_configuration[DatabaseConfig.USER.value],
            password = database_configuration[DatabaseConfig.PASSWORD.value],
            authSource = "admin"
        )

    def get_storage_collection(self) -> Collection:
        return self.client.sylva.storage