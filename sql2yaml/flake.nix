{
  description = "DB-to-YAML Converter for geodetic.isotc211.org";
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    devshell.url = "github:numtide/devshell/main";
    flake-compat = {
      url = "github:edolstra/flake-compat";
      flake = false;
    };
  };
  outputs =
    { self
    , nixpkgs
    , flake-utils
    , devshell
    , flake-compat
    , ...
    }:
    flake-utils.lib.eachDefaultSystem (system:
    let
      cwd = builtins.toString ./.;
      overlays = map (x: x.overlays.default) [
        devshell
      ];
      pkgs = import nixpkgs { inherit system overlays; };
      python = pkgs.python3.withPackages (p: with p; [
        black
        ipython
        javaobj-py3
        jedi-language-server
        pip
        psycopg2
        pylsp-mypy
        python-lsp-ruff
        pyyaml
        virtualenvwrapper
        wheel
      ]);

      buildInputs = with pkgs; [
        bzip2
        clang
        expat
        gdbm
        libffi
        # llvmPackages_16.bintools
        mpdecimal
        ncurses
        openssl
        readline
        rustup
        sqlite
        xz
        zlib
      ];
      lib-path = with pkgs; lib.makeLibraryPath buildInputs;
      openssl-lib-path = with pkgs; lib.makeLibraryPath [ openssl ];

    in
    rec {

      devShell = pkgs.devshell.mkShell {

        # See:
        # https://wiki.nixos.org/wiki/Python#Using_a_Python_package_not_in_Nixpkgs

        # devshell.startup.init1.text = ''
        #   # Allow the use of wheels.
        #   SOURCE_DATE_EPOCH=$(date +%s)

        #   # Augment the dynamic linker path
        #   export "LD_LIBRARY_PATH=$LD_LIBRARY_PATH:${lib-path}"
        #   export "LDFLAGS=-L${openssl-lib-path}:$LDFLAGS"

        #   # Setup the virtual environment if it doesn't already exist.
        #   if [[ ! -d "$VENV" ]]; then
        #     virtualenv $VENV
        #   fi

        #   source ./"$VENV"/bin/activate
        #   export PYTHONPATH="$PYTHONPATH":`pwd`/"$VENV"/${python.sitePackages}/
        # '';

        env = [
          {
            name = "VENV";
            value = ".venv";
          }
          {
            name = "PGDATA";
            value = ".pgsql/data";
          }
        ];
        commands = [
          {
            name = "init";
            command = ''
              [[ -d "$PGDATA" ]] || initdb -D "$PGDATA" "$@"
              [[ -f ./config.py ]] || cp ./config.py.sample ./config.py
              [[ -f ./run.conf ]] || cp ./run.conf.sample ./run.conf
            '';
            help = "Initialize the Postgresql DB";
            category = "Converter";
          }
          {
            name = "startdb";
            command = "pg_ctl -l logfile start \"$@\"";
            help = "Start the Postgresql DB";
            category = "Converter";
          }
          {
            name = "restore";
            command = ''
              if [[ $# -lt 1 ]]; then
                echo "Usage: $0 <dumpfile>"
                exit 1
              fi
              dropdb --if-exists tmp
              createdb tmp
              pg_restore --create --clean --no-owner --no-privileges -d tmp "$@";
            '';
            help = "Restore the Postgresql DB from specified dump file";
            category = "Converter";
          }
          {
            name = "stopdb";
            command = "pg_ctl stop \"$@\"";
            help = "Stop the Postgresql DB";
            category = "Converter";
          }
          {
            name = "convert";
            command = "dump.py \"$@\"";
            help = "Convert the SQL DB into YAML";
            category = "Converter";
          }
          {
            name = "shell";
            command = "psql isoregistry \"$@\"";
            help = "Connect to Postgresql DB";
            category = "Converter";
          }
        ];
        packages = with pkgs; [
          bash
          curl
          fd
          fzf
          gnused
          jq
          postgresql
          python
          ripgrep
          ruff
          wget
        ] ++ buildInputs;
      };
    });
}
