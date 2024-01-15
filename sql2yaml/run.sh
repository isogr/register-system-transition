#!/bin/bash

objects=()

source run.conf

########################################

function zip_dir {
    if [ -n "${1}" ] && [ -d "${output_dir}/${1}" ]
    then
        cd "${output_dir}"
        zip -9 -r "${1}.zip" "${1}"
        cd "${this_dir}"
    fi
}

function clear_dumped_yamls {
    if [ -n "${1}" ] && [ -d "${output_dir}/${1}" ]
    then
        rm -rf "${output_dir}/${1}/"*
    fi

    if [ -e "${output_dir}/${1}.zip" ]
    then
        rm "${output_dir}/${1}.zip"
    fi
}

########################################

this_dir=`pwd`
output_dir="${this_dir}/out"

for object_name in "${objects[@]}"
do
    clear_dumped_yamls "${object_name}"
done

${this_dir}/venv/bin/python3 dump.py -o "${objects[*]}"

if $make_zip_archive
then
    for object_name in "${objects[@]}"
    do
        zip_dir "${object_name}"
    done
fi
