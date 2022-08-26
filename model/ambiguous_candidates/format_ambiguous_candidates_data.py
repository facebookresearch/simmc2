#! /usr/bin/env python
"""
Copyright (c) Facebook, Inc. and its affiliates.
All rights reserved.
This source code is licensed under the license found in the LICENSE file in the
root directory of this source tree.

Reads SIMMC 2.1 dataset, creates train, devtest, dev formats for ambiguous candidates.

Author(s): Satwik Kottur
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import argparse
import copy
import json
import os


SPLITS = ["train", "dev", "devtest", "teststd"]


def get_image_name(scene_ids, turn_ind):
    """Given scene ids and turn index, get the image name.
    """
    sorted_scene_ids = sorted(
        ((int(key), val) for key, val in scene_ids.items()),
        key=lambda x: x[0],
        reverse=True
    )
    # NOTE: Hardcoded to only two scenes.
    if turn_ind >= sorted_scene_ids[0][0]:
        scene_label = sorted_scene_ids[0][1]
    else:
        scene_label = sorted_scene_ids[1][1]
    image_label = scene_label
    if "m_" in scene_label:
        image_label = image_label.replace("m_", "")
    return f"{image_label}.png", scene_label


def get_object_mapping(scene_label, args):
    """Get the object mapping for a given scene.
    """
    scene_json_path = os.path.join(
        args["scene_json_folder"], f"{scene_label}_scene.json"
    )
    with open(scene_json_path, "r") as file_id:
        scene_objects = json.load(file_id)["scenes"][0]["objects"]
    object_map = [ii["index"] for ii in scene_objects]
    return object_map


def main(args):
    for split in SPLITS:
        read_path = args[f"simmc_{split}_json"]
        print(f"Reading: {read_path}")
        with open(read_path, "r") as file_id:
            dialogs = json.load(file_id)

        # Reformat into simple strings with positive and negative labels.
        # (dialog string, label)
        ambiguous_candidates_data = []
        for dialog_id, dialog_datum in enumerate(dialogs["dialogue_data"]):
            history = []
            for turn_ind, turn_datum in enumerate(dialog_datum["dialogue"]):
                history.append(turn_datum["transcript"])

                annotations = turn_datum["transcript_annotated"]
                if annotations.get("disambiguation_label", False):
                    label = annotations["disambiguation_candidates"]
                    image_name, scene_label = get_image_name(
                        dialog_datum["scene_ids"], turn_ind
                    )
                    # If dialog contains multiple scenes, map it accordingly.
                    object_map = get_object_mapping(scene_label, args)
                    new_datum = {
                        "dialog_id": dialog_datum["dialogue_idx"],
                        "turn_id": turn_ind,
                        "input_text": copy.deepcopy(history),
                        "ambiguous_candidates": label,
                        "image_name": image_name,
                        "object_map": object_map,
                    }
                    ambiguous_candidates_data.append(new_datum)
                # Ignore if system_transcript is not found (last round teststd).
                if turn_datum.get("system_transcript", None):
                    history.append(turn_datum["system_transcript"])

        print(f"# instances [{split}]: {len(ambiguous_candidates_data)}")
        save_path = os.path.join(
            args["ambiguous_candidates_save_path"],
            f"simmc2.1_ambiguous_candidates_dstc11_{split}.json"
        )
        print(f"Saving: {save_path}")
        with open(save_path, "w") as file_id:
            json.dump(ambiguous_candidates_data, file_id)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--simmc_train_json", default=None, help="Path to SIMMC 2.1 train"
    )
    parser.add_argument(
        "--simmc_dev_json", default=None, help="Path to SIMMC 2.1 dev"
    )
    parser.add_argument(
        "--simmc_devtest_json", default=None, help="Path to SIMMC 2.1 devtest"
    )
    parser.add_argument(
        "--simmc_teststd_json", default=None, help="Path to SIMMC 2.1 teststd (public)"
    )
    parser.add_argument(
        "--scene_json_folder", default=None, help="Path to SIMMC scene jsons"
    )
    parser.add_argument(
        "--ambiguous_candidates_save_path",
        required=True,
        help="Path to save SIMMC disambiguate JSONs",
    )

    try:
        parsed_args = vars(parser.parse_args())
    except (IOError) as msg:
        parser.error(str(msg))
    main(parsed_args)
