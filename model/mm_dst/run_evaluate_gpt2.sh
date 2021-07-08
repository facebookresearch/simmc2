#!/bin/bash
if [[ $# -lt 1 ]]
then
    PATH_DIR=$(realpath .)
else
    PATH_DIR=$(realpath "$1")
fi

# Evaluate (multi-modal)
#--input_path_predicted="${PATH_DIR}"/gpt2_dst/results/simmc2_dials_devtest_predicted.txt \
#--input_path_predicted="${PATH_DIR}"/gpt2_dst/data/simmc2_dials_devtest_target.txt \
# python -m gpt2_dst.scripts.evaluate \
#     --input_path_target="${PATH_DIR}"/gpt2_dst/data/simmc2_dials_devtest_target.txt \
#     --input_path_predicted="${PATH_DIR}"/gpt2_dst/data/simmc2_dials_devtest_target.txt \
#     --output_path_report="${PATH_DIR}"/gpt2_dst/results/simmc2_dials_devtest_report.json

python -m gpt2_dst.scripts.evaluate_response \
    --input_path_target="${PATH_DIR}"/gpt2_dst/data/simmc2_dials_devtest_target_nobelief.txt \
    --input_path_predicted="${PATH_DIR}"/gpt2_dst/results/simmc2_dials_devtest_predicted.txt
