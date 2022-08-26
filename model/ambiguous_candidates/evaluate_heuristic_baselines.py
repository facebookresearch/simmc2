#! /usr/bin/env python
"""
Evaluate heuristic baselines for SIMMC 2.1 ambigious candidate idenfitication.

Author(s): Satwik Kottur
"""

from __future__ import absolute_import, division, print_function, unicode_literals
import argparse
import json

import torch
import torch.nn as nn
import transformers
from tqdm import tqdm as progressbar

from dataloader import Dataloader
from train_model import evaluate_model


class HeuristicBaseline:
    """Heuristic baseline for ambiguous candidate identification."""

    def __init__(self, scene_json_folder, baseline_type="random"):
        self._type = baseline_type
        self.BASELINE_FORWARD = {
            "random": self.random_baseline,
            "all_objects": self.all_objects_baseline,
            "no_objects": self.no_objects_baseline,
        }
        assert baseline_type in self.BASELINE_FORWARD, f"Invalid: {baseline_type}!"
        self.forward = self.BASELINE_FORWARD[baseline_type]
        self.read_scene_jsons(scene_json_folder)

    def read_scene_jsons(self, scene_json_folder):
        """Given path to scene JSONs, read and index."""
        pass

    def __call__(self, batch):
        return self.forward(batch)

    def random_baseline(self, batch):
        # Return random -1 and 1s.
        return [2 * torch.randint(0, 2, (len(ii),)) - 1 for ii in batch["object_map"]]

    def all_objects_baseline(self, batch):
        # Return all 1 to return all objects.
        return [torch.ones(len(ii)) for ii in batch["object_map"]]

    def no_objects_baseline(self, batch):
        # Return all -1 to return no object.
        return [-1 * torch.ones(len(ii)) for ii in batch["object_map"]]


def main(args):
    args["use_gpu"] = False
    args["max_turns"] = 2
    args["max_length"] = 256
    batch_size = 10
    # Initialize a dummy tokenizer.
    tokenizer = transformers.BertTokenizer.from_pretrained("bert-base-uncased")
    devtest_loader = Dataloader(tokenizer, None, args["devtest_file"], args)
    model = HeuristicBaseline(args["scene_json_folder"], args["baseline_type"])
    recall, precision, f1 = evaluate_model(model, devtest_loader, batch_size, None)

    # Check if performance is the best.
    print(
        f"[devtest]  Rec: {recall:.4f}  " f"|  Prec: {precision:.4f}  |  F1: {f1:.4f}"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--train_file", required=True, help="Path to train file")
    parser.add_argument("--dev_file", required=True, help="Path to dev file")
    parser.add_argument("--devtest_file", required=True, help="Path to devtest file")
    parser.add_argument(
        "--teststd_file", required=True, help="Path to public teststd file"
    )
    parser.add_argument(
        "--scene_json_folder", default=None, help="Path to scene JSON files"
    )
    parser.add_argument(
        "--result_save_path", default=None, help="Path to save devtest results"
    )
    parser.add_argument(
        "--baseline_type",
        default="random",
        choices=["random", "all_objects", "no_objects"],
        help="Type of heuristic baseline",
    )
    try:
        parsed_args = vars(parser.parse_args())
    except (IOError) as msg:
        parser.error(str(msg))
    main(parsed_args)
