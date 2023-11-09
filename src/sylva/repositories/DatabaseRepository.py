import typing
import os
from datetime import datetime, timezone

from pymongo import MongoClient
from pymongo.collection import Collection

from sylva.Configuration import DatabaseConfig
from sylva.Configuration import Configuration
from sylva.MetaData import MetaData


class DatabaseRepository:
    client = None

    def __init__(self, configuration: Configuration) -> None:
        database_configuration = configuration.get_database_config()

        self.client = MongoClient(database_configuration[DatabaseConfig.HOST.value], port=database_configuration[DatabaseConfig.PORT.value], username=database_configuration[DatabaseConfig.USER.value], password=database_configuration[DatabaseConfig.PASSWORD.value], authSource="admin", tz_aware=True)

    def get_storage_collection(self) -> Collection:
        return self.client.sylva.storage

    def get_oldest_non_archived_meta_data(self, limit: int = 20) -> typing.List[MetaData]:
        return list(map(lambda x: MetaData.from_dict(x), self.get_storage_collection().aggregate([{"$match": {"isArchived": False}}, {"$sort": {"end": 1}}, {"$limit": limit}])))

    def set_archived_by_files(self, files: typing.List[str]) -> int:
        modified_count = 0

        for file in files:
            path_seg = os.path.dirname(file)
            file_name_seg = os.path.basename(file)

            update_result = self.get_storage_collection().update_one({"fileName": file_name_seg, "filePath": path_seg}, { "$set": { "isArchived": True, "archivedOn": datetime.now(timezone.utc)} })
            modified_count += update_result.modified_count

        return modified_count