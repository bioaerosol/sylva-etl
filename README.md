[![Test Debian Package](https://github.com/bioaerosol/sylva-etl/actions/workflows/test-debian-package.yml/badge.svg)](https://github.com/bioaerosol/sylva-etl/actions/workflows/test-debian-package.yml)  [![Release Debian Package](https://github.com/bioaerosol/sylva-etl/actions/workflows/release-debian-package.yml/badge.svg)](https://github.com/bioaerosol/sylva-etl/actions/workflows/release-debian-package.yml)

# Overview
SYLVA ETL is a debian package that provides tools to perform the SYLVA data flow. There are two types of storages:

1. Storage – Disk storage for fast access. Holds raw data files of last n days and raw data files that have been made accessible from archive upon request.

2. Archive – Tape archive for long-term storage. Holds all raw data files.

Provided commands are:
1. ```sylva-store``` – Copies raw data files from incoming directory to storage. If configured, hooks will be called for each processed file. This mechanism provides the capability to do device type specific processing after a file has been put to storage. If a hook is configured the file will be put to hook’s STDIN. Calling the hook is a one-shot and output will be logged. By default, this command is called by sylva-etl cronjob.

2. ```sylva-archive``` – Archives files from storage to tape archive. By default, this command is called by sylva-etl cronjob.

3. ```sylva-clean``` – Clean storage by removing files that contain data older than n days (default: 60 days) if they have been put to archive sucessfully. By default, this command is called by sylva-etl cronjob.

4. ```sylva-restore``` Retrieves requested files form archive if they are not in storage anymore. 

5. ```sylva-update-index``` Walks through storage and updates database index according to real exitsing file if this file is found in database index. Can be used if new attributes for index were introduced and you need to run an update on all database index entries.

For help please refer to ```COMMAND --help```, e.g. ```sylva-store --help```.

# Installation
## MongoDB
This package uses a MongoDB which access data is to be configured in /etc/sylva/sylva-config.yaml.
Its up to you to install an appropriate database. For Ubuntu it could look like this.
```
sudo apt install mongodb
```
Then, enable MongoDBs access control as descriped at https://www.mongodb.com/docs/v3.4/tutorial/enable-authentication. This package will create its collections in a database called "sylva". That's why you should create a dedicated user to be used by this package which has readWrite access to database "sylva", e.g.
```
use admin
db.createUser(
    {
        user: "sylva", 
        pwd: "changeit", 
        roles: [ { role: "readWrite", db: "sylva" } ]
    }
)
```

## Debian Package (this)
### Download
To install latest release provide a GitHub PAT as environment variable $GITHUBPAT (as long as this repo is not public)
```
GITHUBPAT=<PAT>
```
and then download latest release using this command:
```
wget -O $(curl -H "Authorization: token $GITHUBPAT" -s https://api.github.com/repos/bioaerosol/sylva-etl/releases/latest | jq '.assets[] | select(.name | endswith(".deb")) | .name' | tr -d '"') --header "Authorization: token $GITHUBPAT" --header "Accept: application/octet-stream" $(curl -H "Authorization: token $GITHUBPAT" -s https://api.github.com/repos/bioaerosol/sylva-etl/releases/latest | jq '.assets[] | select(.name | endswith(".deb")) | .url' | tr -d '"')
```
### Installation
Package can be installed as any other Debian package, e.g.:
```
sudo apt install <package-file>
```
# Configuration
The package is configured in two YAML files in /etc/sylva:

## Package Configuration
| Key | Description |
| --- | --- |
| sylva-etl.enabled | Set to true to run sylva-store automatically |
| sylva-etl.archive-enabled | Set to true to run sylva-archive automatically |
| sylva-etl.clean-enabled | Set to true to run sylva-clean automatically |
| clean.clean-older-than-days | Data will be cleaned if it is older than this value (days) |
| database.host | Host of MongoDB |
| database.port | Port of MongoDB |
| database.user | User to access MongoDB |
| database.password | Password to access MongoDB |
| folders.incoming | Path to incoming folder |
| folders.storage | Path to storage folder |
| folders.trash | Path to trash folder |

Example with default values:
```yaml
sylva-etl:
  enabled: false
  archive-enabled: false
  clean-enabled: false
clean:
  clean-older-than-days: 60
database:
  host: localhost
  port: 27017
  user: sylva
  password: changeit
folders:
  incoming: /home/sylva/incoming
  storage: /home/sylva/storage
  trash: /home/sylva/trash
hooks:
```
## Device Configuration
| Key | Description |
| --- | --- |
| locations | Array of locations where devices are installed |
| locations[n].name | Name of the location. |
| locations[n].hooks | List of hooks to be applied for files of this location. |
| locations[n].devices | Array of devices installed at this location |
| locations[n].devices[n].BAA500 | Array of BAA500 devces installed at this location. Array contains entries of type string that refer to the ID of the devices installed at this location. |
| locations[n].devices[n].Poleno | Array of Poleno devces installed at this location. Array contains entries of type string that refer to the ID of the devices installed at this location. |

Example with some random values:
```yaml
locations:
- name: DEUFS
  devices:
    Poleno:
      - "poleno-1"
  hooks:
    - date
```

