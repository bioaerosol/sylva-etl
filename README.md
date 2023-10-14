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