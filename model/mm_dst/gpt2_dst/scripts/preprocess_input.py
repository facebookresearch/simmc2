#!/usr/bin/env python3
"""
Copyright (c) Facebook, Inc. and its affiliates.
All rights reserved.
This source code is licensed under the license found in the LICENSE file in the
root directory of this source tree.

    Scripts for converting the main SIMMC datasets (.JSON format)
    into the line-by-line stringified format (and back).

    The reformatted data is used as input for the GPT-2 based
    DST model baseline.
"""
from gpt2_dst.utils.convert import convert_json_to_flattened
import argparse


if __name__ == "__main__":
    # Parse input args
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input_path_json", help="input path to the original dialog data"
    )
    parser.add_argument("--output_path_predict", help="output path for model input")
    parser.add_argument("--output_path_target", help="output path for full target")
    parser.add_argument(
        "--input_path_special_tokens",
        help="input path for special tokens. blank if not provided",
        default="",
    )
    parser.add_argument(
        "--output_path_special_tokens",
        help="output path for special tokens. blank if not saving",
        default="",
    )
    parser.add_argument(
        "--len_context",
        help="# of turns to include as dialog context",
        type=int,
        default=2,
    )
    parser.add_argument(
        "--use_multimodal_contexts",
        help="determine whether to use the multimodal contexts each turn",
        type=int,
        default=1,
    )
    parser.add_argument(
        "--no_belief_states",
        dest="use_belief_states",
        action="store_false",
        default=True,
        help="determine whether to use belief state for each turn",
    )
    parser.add_argument(
        "--no_target",
        dest="output_target",
        action="store_false",
        default=True,
        help="determine whether to output a formatted output for Target",                
    )

    # Options for retrieval evaluation.
    parser.add_argument(
        "--input_path_retrieval", help="input path to the retrieval candidates",
    )
    parser.add_argument(
        "--output_path_retrieval", help="output path to retrieval candidates",
    )

    args = parser.parse_args()
    input_path_json = args.input_path_json
    output_path_predict = args.output_path_predict
    output_path_target = args.output_path_target
    input_path_special_tokens = args.input_path_special_tokens
    output_path_special_tokens = args.output_path_special_tokens
    len_context = args.len_context
    use_multimodal_contexts = bool(args.use_multimodal_contexts)
    # Retrieval encoding arguments.
    input_path_retrieval = args.input_path_retrieval
    output_path_retrieval = args.output_path_retrieval

    # DEBUG:
    print("Belief states: {}".format(args.use_belief_states))

    # Convert the data into GPT-2 friendly format
    convert_json_to_flattened(
        input_path_json,
        output_path_predict,
        output_path_target,
        input_path_special_tokens=input_path_special_tokens,
        output_path_special_tokens=output_path_special_tokens,
        len_context=len_context,
        use_multimodal_contexts=use_multimodal_contexts,
        use_belief_states=args.use_belief_states,
        output_target=args.output_target,
        input_path_retrieval=input_path_retrieval,
        output_path_retrieval=output_path_retrieval,
    )
