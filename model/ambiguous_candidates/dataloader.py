#! /usr/bin/env python
"""
Copyright (c) Facebook, Inc. and its affiliates.
All rights reserved.
This source code is licensed under the license found in the LICENSE file in the
root directory of this source tree.

Dataloader for ambiguous candidates identification task on SIMMC 2.1.

Author(s): Satwik Kottur
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import json

import numpy as np
import torch


class Dataloader:
    def __init__(self, tokenizer, feature_loader, load_path, args, hidden_labels=False):
        self._tokenizer = tokenizer
        self._features = feature_loader
        self._args = args
        self._hidden_labels = hidden_labels
        print("Loading: {}".format(load_path))
        with open(load_path, "r") as file_id:
            self._raw_data = json.load(file_id)
        # Also read the source data for evaluation.
        with open(self._raw_data["source_path"], "r") as file_id:
            self.source_data = json.load(file_id)
        self._data = self._raw_data["data"]

        self.num_utterances = 2 * args["max_turns"] + 1
        self.num_instances = len(self._data)
        self.device = torch.cuda if args["use_gpu"] else torch

    def get_random_batch(self, batch_size):
        indices = np.random.randint(0, self.num_instances, batch_size)
        return self.get_indexed_data(indices)

    def get_entire_batch(self, batch_size):
        all_indices = np.arange(self.num_instances)
        for start in all_indices[::batch_size]:
            batch_indices = all_indices[start : start + batch_size]
            yield self.get_indexed_data(batch_indices)

    def get_indexed_data(self, indices):
        text_labels = []
        text_inputs = []
        dialog_ids = []
        turn_ids = []
        features = []
        object_maps = []
        for index in indices:
            # Add <USER> and <SYS> tokens.
            dialog_datum = self._data[index]
            dialog = self._data[index]["input_text"]
            for turn_id, turn in enumerate(dialog):
                if turn_id % 2 == 0:
                    dialog[turn_id] = "<USER> " + turn
                else:
                    dialog[turn_id] = "<SYS> " + turn
            text = " ".join(dialog[-self.num_utterances :])
            text_inputs.append(text)
            dialog_ids.append(dialog_datum["dialog_id"])
            turn_ids.append(dialog_datum["turn_id"])
            object_map = dialog_datum["object_map"]
            # Get image features.
            if self._features:
                features.append(self._features[dialog_datum["image_name"]])
                num_candidates = features[-1].shape[0]
            else:
                num_candidates = len(object_map)

            # Get the ambiguous candidates and map it local ids.
            global_ambiguous_candidates = dialog_datum["ambiguous_candidates"]
            local_ambiguous_candidates = [
                object_map.index(ii) for ii in global_ambiguous_candidates
            ]
            # NOTE: Few scenes have misaligned image features (ignore them).
            # Default object map to linear local ids in such cases.
            if len(object_map) != num_candidates:
                local_ambiguous_candidates = global_ambiguous_candidates
                object_map = list(range(num_candidates))
            object_maps.append(object_map)
            label = torch.tensor(
                [
                    1 if ii in local_ambiguous_candidates else 0
                    for ii in range(num_candidates)
                ],
                dtype=torch.float32,
            )
            text_labels.append(label)

        encoded_inputs = self._tokenizer(
            text_inputs,
            padding=True,
            max_length=self._args["max_length"],
            return_tensors="pt",
            truncation=True,
        )
        encoded_inputs = {key: val.detach() for key, val in encoded_inputs.items()}
        if self._args["use_gpu"]:
            encoded_inputs = {key: val.cuda() for key, val in encoded_inputs.items()}
            text_labels = [ii.cuda() for ii in text_labels]
        if self._hidden_labels:
            # Reset all the text_labels to [0] (dummy labels).
            text_labels = [[0] for ii in text_labels]

        # Pack the batch.
        batch = {
            "text_in": encoded_inputs,
            "gt_label": text_labels,
            "dialog_id": dialog_ids,
            "turn_id": turn_ids,
            "features": features,
            "object_map": object_maps,
        }
        return batch


class VisualFeatureLoader:
    """Loads visual features for SIMMC 2.1 ambiguous candidate identification."""

    UNAVAILABLE_IMAGES = [
        "cloth_store_1416238_woman_20_6.png",
        "cloth_store_1416238_woman_19_0.png",
        "cloth_store_1416238_woman_4_8.png",
    ]

    def __init__(self, feature_path, feature_size):
        """Read the features from the path."""
        self._features = torch.load(feature_path)
        self._feature_size = feature_size
        self._zero_feature = torch.zeros((1, self._feature_size), dtype=torch.float)

    def __getitem__(self, label):
        """Get the feature given image label."""
        assert (
            label in self._features or label in self.UNAVAILABLE_IMAGES
        ), f"{label} not found!"
        if label in self.UNAVAILABLE_IMAGES:
            return self._zero_feature
        return self._features[label]

    def cuda(self):
        """Move the features to cuda."""
        self._zero_feature = self._zero_feature.cuda()
        for key, val in self._features.items():
            self._features[key] = val.cuda()
