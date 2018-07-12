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
for folder in $(ls -d ${IN_FOLDER}*/); do
    echo "Running benchmark on ${folder}"
    for file in $(ls ${folder}); do
        echo -n "${folder}${file}..."
        timeout 15m python benchmark.py ${folder}${file}
        echo " done"
    done
done
