import yaml


class DevicesRepository:
    __configuration = []

    def __init__(self, configuration_file="/etc/sylva-etl/sylva-devices.yaml") -> None:
        with open(configuration_file, "r") as cf:
            self.__configuration = yaml.load(cf, Loader=yaml.FullLoader)

    def get_location_for(self, device_type: str, device_id: str) -> str:
        for location in self.__configuration["locations"]:
            if device_type in location["devices"]:
                try:
                    if location["devices"][device_type].index(device_id) >= 0:
                        return location["name"]
                except ValueError:
                    pass

        raise ValueError("Cannot find device location for type {0} and id {1}.".format(device_type, device_id))
    
    def get_hooks_for(self, device_location: str) -> list:
        for location in self.__configuration["locations"]:
            if location["name"] == device_location:                
                return location["hooks"] or [] if "hooks" in location else []

        return []
