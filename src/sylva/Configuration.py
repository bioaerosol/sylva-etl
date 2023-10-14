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
    ARCHIVE = "archive"
    TRASH = "trash"

class Configuration():
    __configuration = []

    def __init__(self, configuration_file="/etc/sylva/sylva-config.yaml") -> None:
        with open(configuration_file, 'r') as cf:
            self.__configuration = yaml.load(cf, Loader=yaml.FullLoader)

    def get_database_config(self):
        return self.__configuration["database"]
    
    def get_folders(self):
        return self.__configuration["folders"]
