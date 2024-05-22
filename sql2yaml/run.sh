#!/bin/bash

objects=()

source run.conf

########################################

clean_up() {
    for object_name in "$@"
    do
        clear_dumped_yamls "${object_name}"
    done
}

clear_dumped_yamls() {
    local object_name="${1:?Missing object name}"

    if [[ -d "${output_dir}/${object_name}" ]]
    then
        rm -rf "${output_dir}/${object_name:?}/"*
    fi

    if [[ -e "${output_dir}/${object_name}.zip" ]]
    then
        rm "${output_dir}/${object_name:?}.zip"
    fi
}

zip_up() {
    local make_zip_archive=$1
    shift

    if $make_zip_archive
    then
        for object_name in "$@"
        do
            zip_dir "${object_name}"
        done
    fi
}

zip_dir() {
    local object_name="${1:?Missing object name}"

    if [[ -d "${output_dir}/${object_name}" ]]
    then
        pushd "${output_dir}"
        zip -9 -r "${object_name}.zip" "${object_name}"
        popd
    fi
}

########################################

declare output_dir="${PWD}/out"

main() {
    selected_objects=()

    if command -v fzf >/dev/null 2>&1 && [[ "$1" = -s ]]
    then
        while IFS= read -r selected_object
        do
            selected_objects+=("${selected_object}")
        done < <(for o in "${objects[@]}"; do echo "$o"; done | fzf --multi)
    else
        selected_objects=("${objects[@]}")
    fi

    clean_up "${selected_objects[@]}"
    ./dump.py -o "${selected_objects[*]}"
    zip_up "${make_zip_archive}" "${selected_objects[@]}"
}

main "$@"
