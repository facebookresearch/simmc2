#!/bin/bash
if [[ $# -lt 1 ]]
then
    PATH_DIR=$(realpath .)
    PATH_DATA_DIR=$(realpath ../data)
else
    PATH_DIR=$(realpath "$1")
    PATH_DATA_DIR=$(realpath "$2")
fi

# Fashion
# Multimodal Data
# Train split
python -m gpt2_dst.scripts.preprocess_input \
    --input_path_json="${PATH_DATA_DIR}"/simmc2_dials_train.json \
    --output_path_predict="${PATH_DIR}"/gpt2_dst/data/simmc2_dials_train_predict_nobelief.txt \
    --output_path_target="${PATH_DIR}"/gpt2_dst/data/simmc2_dials_train_target_nobelief.txt \
    --len_context=2 \
    --use_multimodal_contexts=0 --no_belief_states\
    --output_path_special_tokens="${PATH_DIR}"/gpt2_dst/data/simmc2_special_tokens.json

# --use_multimodal_contexts=1 \
# Dev split
python -m gpt2_dst.scripts.preprocess_input \
    --input_path_json="${PATH_DATA_DIR}"/simmc2_dials_dev.json \
    --output_path_predict="${PATH_DIR}"/gpt2_dst/data/simmc2_dials_dev_predict_nobelief.txt \
    --output_path_target="${PATH_DIR}"/gpt2_dst/data/simmc2_dials_dev_target_nobelief.txt \
    --len_context=2 \
    --use_multimodal_contexts=0 --no_belief_states\
    --input_path_special_tokens="${PATH_DIR}"/gpt2_dst/data/simmc2_special_tokens.json \
    --output_path_special_tokens="${PATH_DIR}"/gpt2_dst/data/simmc2_special_tokens.json \

# Devtest split
python -m gpt2_dst.scripts.preprocess_input \
    --input_path_json="${PATH_DATA_DIR}"/simmc2_dials_devtest.json \
    --output_path_predict="${PATH_DIR}"/gpt2_dst/data/simmc2_dials_devtest_predict_nobelief.txt \
    --output_path_target="${PATH_DIR}"/gpt2_dst/data/simmc2_dials_devtest_target_nobelief.txt \
    --len_context=2 \
    --use_multimodal_contexts=0 --no_belief_states\
    --input_path_special_tokens="${PATH_DIR}"/gpt2_dst/data/simmc2_special_tokens.json \
    --output_path_special_tokens="${PATH_DIR}"/gpt2_dst/data/simmc2_special_tokens.json \

# Test split
python -m gpt2_dst.scripts.preprocess_input \
    --input_path_json="${PATH_DATA_DIR}"/simmc2_dials_test.json \
    --output_path_predict="${PATH_DIR}"/gpt2_dst/data/simmc2_dials_test_predict_nobelief.txt \
    --output_path_target="${PATH_DIR}"/gpt2_dst/data/simmc2_dials_test_target_nobelief.txt \
    --len_context=2 \
    --use_multimodal_contexts=0 --no_belief_states\
    --input_path_special_tokens="${PATH_DIR}"/gpt2_dst/data/simmc2_special_tokens.json \
    --output_path_special_tokens="${PATH_DIR}"/gpt2_dst/data/simmc2_special_tokens.json \

# Mini split
python -m gpt2_dst.scripts.preprocess_input \
    --input_path_json="${PATH_DATA_DIR}"/simmc2_dials_mini.json \
    --output_path_predict="${PATH_DIR}"/gpt2_dst/data/simmc2_dials_mini_predict_nobelief.txt \
    --output_path_target="${PATH_DIR}"/gpt2_dst/data/simmc2_dials_mini_target_nobelief.txt \
    --len_context=2 \
    --use_multimodal_contexts=0 --no_belief_states\
    --input_path_special_tokens="${PATH_DIR}"/gpt2_dst/data/simmc2_special_tokens.json \
    --output_path_special_tokens="${PATH_DIR}"/gpt2_dst/data/simmc2_special_tokens.json \
