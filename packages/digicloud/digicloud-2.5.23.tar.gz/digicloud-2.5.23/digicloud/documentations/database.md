Database, Digicloud database as a service (DBAAS)

DigiCloud database services are called  **database**


## Examples:

1. **list available instance types**

    The following command can be used for listing available instance types, one should choose one of
    these types for dbaas instance creation.

        $ digicloud instance type list
2. **list available datastore name and version**
    
    The following command can be used for listing available datastore name and version, one should choose one of 
    these name and version for dbaas instance creation.

        $ digicloud database datastore list
3. **Create database instance**
    
    During database instance creation, it's required to specify the datastore name, version, and network. 
    To make the database publicly accessible, use the --is-public flag. You can also control access by 
    limiting it to specific IP ranges with the --allow-cidr option, giving you greater flexibility in 
    managing who can connect to your DBAAS instance.

        # create dbaas instance without public access
        $ digicloud database instance create my_instance \
                     --instance-type g1.medium \
                     --network my_network \
                     --volume-type SSD \
                     --volume-size 20 \
                     --datastore-name mysql \
                     --datastore-version 5.7.29 \
    or

        # create dbaas instance with public access
        $ digicloud database instance create my_instance \
                     --instance-type g1.medium \
                     --network my_network \
                     --volume-type SSD \
                     --volume-size 20 \
                     --datastore-name mysql \
                     --datastore-version 5.7.29 \
                     --is-public
    or

        # create dbaas instance without limit access with cidr flag
        $ digicloud database instance create my_instance \
                     --instance-type g1.medium \
                     --network my_network \
                     --volume-type SSD \
                     --volume-size 20 \
                     --datastore-name mysql \
                     --datastore-version 5.7.29 \
                     --is-public \
                     --allow-cidr 192.168.1.0/24
4. **List database instances**

    One can list all database instances using the following command.

        $ digicloud database instance list  
5. **details of database instance**

    To view the details of a specific database instance, you can use the following command,
    providing either the instance name or ID.

        $ digicloud database instance show my_instance
6. **delete database instances**

    A database instance can be deleted by providing either its name or ID using the following command.

        $ digicloud database instance delete my_instance
7. **create dbaas database**

    Before creating a database, you must first set up a database instance. Once the instance is ready,
    you can create a new database with the following command.

        $ digicloud database database create --instance my_instance my_database

8. **delete dbaas database**

    Before deleting a database, ensure that the associated database instance is active. To delete a
    database, use the following command.

        $ digicloud database database delete --instance my_instance my_database
9. **list dbaas database**

    Before listing the databases, make sure that the associated database instance is active. To view
    all databases within a specific instance, use the following command.

        $ digicloud database database list --instance my_instance

10. **create dbaas user**

    Before creating a dbaas user, ensure that the associated database instance is active. To create
    a new user for a specific database instance, use the following command.

        $ digicloud database user create --instance my_instance \
                     --username my_user \
                     --password  my_password \
                     --databases my_database \
                     --host 192.168.1.1
11. **delete dbaas user**

    Before deleting a DBAAS user, ensure that you have the necessary permissions and that the user 
    is not currently connected to the database instance. To delete a user, use the following command.

        $ digicloud database user delete --instance my_instance my_user 
11. **list dbaas users**

    To view all users associated with a specific database instance, ensure that the instance is
    active. You can list all users by executing the following command.

        $ digicloud database user list --instance my_instance 

