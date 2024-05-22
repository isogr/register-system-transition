#!/usr/bin/env bash

# May be necessary on some linux distros:
# sudo apt-get update -y
# sudo apt-get install -y python3-psycopg2
# sudo apt-get install -y python3-venv

read -p "Do you wish to create venv, install requirements and configs files? [Y/N]" -n 1 -r

echo ""

if [[ $REPLY =~ ^[Yy]$ ]]
then
    project_dir=$PWD

    python3 -m venv "${project_dir}/venv"

    source "${project_dir}/venv/bin/activate"

    pip3 install --upgrade pip
    pip3 install -r "${project_dir}/requirements.txt"

    cp "${project_dir}/config.py.sample" "${project_dir}/config.py"
    cp "${project_dir}/run.conf.sample" "${project_dir}/run.conf"
else
    echo "Canceled"
fi
