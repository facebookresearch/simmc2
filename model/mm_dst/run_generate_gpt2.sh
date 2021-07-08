#!/bin/bash
if [[ $# -lt 1 ]]
then
    PATH_DIR=$(realpath .)
else
    PATH_DIR=$(realpath "$1")
fi

# Generate sentences (Furniture, multi-modal)
python -m gpt2_dst.scripts.run_generation \
    --model_type=gpt2 \
    --model_name_or_path="${PATH_DIR}"/gpt2_dst/save/model_final_2/checkpoint-14000 \
    --num_return_sequences=1 \
    --length=100 \
    --stop_token='<EOS>' \
    --prompts_from_file="${PATH_DIR}"/gpt2_dst/data/simmc2_dials_devtest_predict_nobelief.txt \
    --path_output="${PATH_DIR}"/gpt2_dst/results/simmc2_dials_devtest_predicted.txt
#     --prompts_from_file="${PATH_DIR}"/gpt2_dst/data/simmc2_dials_devmini_predict_nobelief.txt \
#     --path_output="${PATH_DIR}"/gpt2_dst/results/simmc2_dials_devmini_predicted.txt
