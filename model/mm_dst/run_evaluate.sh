#!/bin/bash
if [[ $# -lt 1 ]]
then
    PATH_DIR=$(realpath .)
    PATH_DATA_DIR=$(realpath ../../data)
else
    PATH_DIR=$(realpath "$1")
    PATH_DATA_DIR=$(realpath "$2")
fi

# Evaluate (Example)
python -m utils.evaluate_dst \
    --input_path_target="${PATH_DATA_DIR}"/simmc2_dials_dstc10_devtest.json \
    --input_path_predicted="${PATH_DIR}"/simmc2_dials_dstc10_devtest_predicted.json \
    --output_path_report="${PATH_DIR}"/simmc2_dials_dstc10_report.json
