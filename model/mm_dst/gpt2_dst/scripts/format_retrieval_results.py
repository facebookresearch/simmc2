#! /usr/bin/env python
"""
Format retrieval outputs into challenge format.

Author(s): Satwik Kottur
"""

from __future__ import absolute_import, division, print_function, unicode_literals
import argparse

import json


NUM_OPTIONS = 100


def main(args):
    print(f"""Reading dialogs: {args["dialog_json_file"]}""")
    with open(args["dialog_json_file"], "r") as file_id:
        dialogs = json.load(file_id)

    print(f"""Reading outputs: {args["model_output_file"]}""")
    with open(args["model_output_file"], "r") as file_id:
        scores = [float(ii) for ii in file_id.readlines()]

    # Number of scores should match number of instances.
    num_turns = sum(len(ii["dialogue"]) for ii in dialogs["dialogue_data"])
    assert len(scores) == NUM_OPTIONS * num_turns, "#turns do not match!"

    formatted_result = []
    num_turns = 0
    for dialog_datum in dialogs["dialogue_data"]:
        dialog_id = dialog_datum["dialogue_idx"]
        new_entry = {"dialog_id": dialog_id, "candidate_scores": []}
        for turn_id, turn_datum in enumerate(dialog_datum["dialogue"]):
            start_ind = num_turns * NUM_OPTIONS
            end_ind = (num_turns + 1) * NUM_OPTIONS

            # Scores are NLL, lower is better, hence -1.
            new_turn_entry = {
                "turn_id": turn_id,
                "scores": [-1 * ii for ii in scores[start_ind:end_ind]],
            }
            num_turns += 1
            new_entry["candidate_scores"].append(new_turn_entry)
        formatted_result.append(new_entry)

    # Write the result back.
    print(f"""Saving: {args["formatted_output_file"]}""")
    with open(args["formatted_output_file"], "w") as file_id:
        json.dump(formatted_result, file_id)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--model_output_file", required=True, help="Model output path",
    )
    parser.add_argument(
        "--dialog_json_file", required=True, help="Original SIMMC dialog JSON",
    )
    parser.add_argument(
        "--formatted_output_file", required=True, help="Formatted model output path"
    )

    try:
        parsed_args = vars(parser.parse_args())
    except (IOError) as msg:
        parser.error(str(msg))
    main(parsed_args)
