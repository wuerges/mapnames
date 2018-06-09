#!/bin/bash

IN_FOLDER=$1
#OUT_FOLDER=$2

if [[ ${IN_FOLDER} != */ ]]; then
    IN_FOLDER=${IN_FOLDER}/
fi

#if [ -z ${OUT_FOLDER} ]; then
#    OUT_FOLDER=./
#fi

echo "Root folder: ${IN_FOLDER}"
for folder in $(ls ${IN_FOLDER}); do
    echo "Running benchmark on ${IN_FOLDER}${folder}"
    for file in $(ls ${IN_FOLDER}${folder}); do
        echo -n "${IN_FOLDER}${folder}/${file}..."
        timeout 15m python benchmark.py ${IN_FOLDER}${folder}/${file}
        echo " done"
    done
done
