[![Test Debian Package](https://github.com/bioaerosol/sylva-etl/actions/workflows/test-debian-package.yml/badge.svg)](https://github.com/bioaerosol/sylva-etl/actions/workflows/test-debian-package.yml)

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
| sylva-etl.enabled | Set to true to run ETL automatically |
| database.host | Host of MongoDB |
| database.port | Port of MongoDB |
| database.user | User to access MongoDB |
| database.password | Password to access MongoDB |
| folders.incoming | Path to incoming folder |
| folders.storage | Path to storage folder |
| folders.trash | Path to trash folder |
| hooks.[monitorType] | List of hooks to bve applied for files from monitors of mentioned type. |

Example with default values:
```yaml
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
  Poleno:
  - md5sum
```
## Device Configuration
| Key | Description |
| --- | --- |
| locations | Array of locations where devices are installed |
| locations[n].name | Name of the location. |
| locations[n].devices | Array of devices installed at this location |
| locations[n].devices[n].BAA500 | Array of BAA500 devces installed at this location. Array contains entries of type string that refer to the ID of the devices installed at this location. |
| locations[n].devices[n].Poleno | Array of Poleno devces installed at this location. Array contains entries of type string that refer to the ID of the devices installed at this location. |

Example with some random values:
```yaml
locations:
- name: Schneefernerhaus
  devices:
    Poleno:
      - "poleno-1"
      - "poleno-2"
    BAA500:
      - "00013"
```

