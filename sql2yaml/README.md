Data migration script that takes SQL data dump and outputs a set of YAML files representing Paneron dataset with the register.

Installation
------------

Make the installation files executable:

```
chmod +x install.sh
chmod +x run.sh
```

Setup the environment using the install.sh file:

```
./install.sh
```

Run the data extraction tool (this will extract all objects).

```
./run.sh
```

Specific objects can be extracted independently using the following command:

```
 python3 dump.py -o [OBJECT_NAMES]
 ```


Troubleshooting
---------------

If running into issue when installing psycopg2 on a MacOS, try installing it manually using the flag:

```
ARCHFLAGS="-arch x86_64" pip install psycopg2
```

and then run the `./install.sh` command again.
