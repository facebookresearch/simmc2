#!/bin/bash
if [[ $# -lt 1 ]]
then
    PATH_DIR=$(realpath .)
else
    PATH_DIR=$(realpath "$1")
fi

# Evaluate (multi-modal)
python -m gpt2_dst.scripts.evaluate \
    --input_path_target="${PATH_DIR}"/gpt2_dst/data/simmc2.1_dials_dstc11_devtest_target.txt \
    --input_path_predicted="${PATH_DIR}"/gpt2_dst/data/simmc2.1_dials_dstc11_devtest_predicted.txt \
    --output_path_report="${PATH_DIR}"/gpt2_dst/results/simmc2.1_dials_dstc11_devtest_report.json

#python -m gpt2_dst.scripts.evaluate_response \
#    --input_path_target="${PATH_DIR}"/gpt2_dst/data/simmc2_dials_dstc10_devtest_target.txt \
#    --input_path_predicted="${PATH_DIR}"/gpt2_dst/results/simmc2_dials_dstc10_devtest_predicted.txt
