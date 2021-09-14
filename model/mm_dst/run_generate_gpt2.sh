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
    --model_name_or_path="${PATH_DIR}"/gpt2_dst/save/model/ \
    --num_return_sequences=1 \
    --length=100 \
    --stop_token='<EOS>' \
    --prompts_from_file="${PATH_DIR}"/gpt2_dst/data/simmc2_dials_dstc10_devtest_predict.txt \
    --path_output="${PATH_DIR}"/gpt2_dst/results/simmc2_dials_dstc10_devtest_predicted.txt


# python -m gpt2_dst.scripts.run_retrieval \
#     --model_type=gpt2 \
#     --length=256 \
#     --model_name_or_path="${PATH_DIR}"/gpt2_dst/save/model/ \
#     --prompts_from_file="${PATH_DIR}"/gpt2_dst/data/simmc2_dials_dstc10_devtest_retrieval.txt \
#     --path_output="${PATH_DIR}"/gpt2_dst/results/simmc2_dials_dstc10_devtest_predicted.txt
