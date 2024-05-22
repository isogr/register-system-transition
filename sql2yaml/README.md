Data migration script that takes SQL data dump and outputs a set of YAML files representing Paneron dataset with the register.

Installation
------------

With [Nix](https://nixos.org/)
([install Nix with flakes enabled](https://github.com/DeterminateSystems/nix-installer)),
simply run the following to enter a shell that has all dependencies taken
care of:

```
> nix develop
```

Otherwise, do the following.

Make the installation files executable:

```
chmod +x install.sh
chmod +x run.sh
```

Setup the environment using the install.sh file:

```
./install.sh
```

Then, make sure to configure the `config.py` file for Postgresql DB access,
or set up the following environmental variables:

```
export PGHOST=127.0.0.1
export PGPORT=5432
export PGUSER=$USER
export PGPASSWORD=#...
export PGDATABASE=isoregistry
```

Usage
-----

Run the data extraction tool (this will extract all objects specified in `run.conf`).

```
./run.sh
```

Specific objects can be extracted independently using the following command:

```
# Open fzf to select multiple objects (select using TAB)
./run.sh -s

# Dump all objects
./dump.py

# or
./dump.py -o OBJECT_NAMES
 ```

Import of Database
------------------

Prerequisites:

- database dump file (`/path/to/db.dump`)
- Postgresql


Initialize Postgresql:

```console
> init                         # if using `nix develop`
```

```console
> export PGDATA=.pgsql/data    # otherwise
> initdb
```


Start Postgresql:

```console
> startdb                    # if using `nix develop`
```

```console
> pg_ctl  -l logfile start   # otherwise
```

Run the following commands to create the database:

```console
> restore /path/to/db.dump    # if using `nix develop`
```

```console
# otherwise
> dropdb tmp ; \
  createdb tmp ; \
  pg_restore --create --clean --no-owner --no-privileges -d tmp /path/to/db.dump
CREATE ROLE
> # done!
```

Stop Postgresql when done:

```console
> stopdb         # if using `nix develop`
```
```console
> pg_ctl stop    # otherwise
```

Troubleshooting
---------------

If running into issue when installing psycopg2 on a MacOS, try installing it manually using the flag:

```
ARCHFLAGS="-arch x86_64" pip install psycopg2
```

and then run the `./install.sh` command again.

Or, if you are in the market for Nix,
[install Nix with flakes enabled](https://github.com/DeterminateSystems/nix-installer),
then simply run the following to enter a shell that has all dependencies taken
care of:

```
> nix develop
```
