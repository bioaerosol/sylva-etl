""" Functions to manage stations. """
import yaml
from enum import Enum

class DatabaseConfig(Enum):
    HOST = "host"
    PORT = "port"
    USER = "user"
    PASSWORD = "password"

class Folder(Enum):
    INCOMING = "incoming"
    STORAGE = "storage"
    TRASH = "trash"

class Configuration():
    __configuration = []

    def __init__(self, configuration_file="/etc/sylva-etl/sylva-config.yaml") -> None:
        with open(configuration_file, 'r') as cf:
            self.__configuration = yaml.load(cf, Loader=yaml.FullLoader)

    def get_database_config(self):
        return self.__configuration["database"]
    
    def get_folders(self):
        return self.__configuration["folders"]
    
    def get_hooks(self, device_type_name: str) -> []:
        if (device_type_name in (self.__configuration["hooks"] or [])):
            return self.__configuration["hooks"][device_type_name]
        else:
            return []
        
    def is_etl_enabled(self) -> bool:
        return self.__configuration["sylva-etl"]["enabled"]
    
    def is_archive_enabled(self) -> bool:
        return self.__configuration["sylva-etl"]["archive-enabled"]