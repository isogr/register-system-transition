#!/bin/bash

# May be necessary on some linux distros:
# sudo apt-get update -y
# sudo apt-get install -y python3-psycopg2

project_dir=`pwd`

python3 -m venv ${project_dir}/venv

source ${project_dir}/venv/bin/activate

pip3 install --upgrade pip
pip3 install -r ${project_dir}/requirements.txt

cp ${project_dir}/config.py.sample ${project_dir}/config.py
cp ${project_dir}/run.conf.sample ${project_dir}/run.conf
