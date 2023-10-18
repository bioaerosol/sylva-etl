# Installation
## MongoDB
This package uses a MongoDB which access data is to be configured in /etc/sylva/sylva-config.yaml.
Its up to you to install an appropriate database. For Ubuntu it could look like this.
```
sudo apt install mongodb
```
Then, enable MongoDBs access control as descriped at https://www.mongodb.com/docs/v3.4/tutorial/enable-authentication. This package will create its colletions in a database called "sylva". That's why you should create a dedicated user to be used by this package which has readWrite access to database "sylva", e.g.
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

# Configuration
The package is configured in two YAML files in /etc/sylva:

## Package Configuration
| Key | Description |
| --- | --- |
| database.host | Host of MongoDB |
| database.port | Port of MongoDB |
| database.user | User to access MongoDB |
| database.password | Password to access MongoDB |
| folders.incoming | Path to incoming folder |
| folders.archive | Path to archive folder |
| folders.trash | Path to trash folder |

Example with default values:
```yaml
database:
  host: localhost
  port: 27017
  user: sylva
  password: changeit
folders:
  incoming: /home/sylva/incoming
  archive: /home/sylva/archive
  trash: /home/sylva/trash
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
    Poleno:
      -  "poleno-3"
```

