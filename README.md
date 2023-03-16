Data Extraction Tools
---------------------
---------------------

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

Run the data extraction tool specifying one of the "objects" to be extracted (you might need to activate the virtual environment manually).

```
python3 dump.py -o 'proposals'
```


Troubleshooting
---------------

If running into issue when installing psycopg2, try installing it manually using:

```
ARCHFLAGS="-arch x86_64" pip install psycopg2
```

and run the `./install.sh` again.
