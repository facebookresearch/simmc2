#! /usr/bin/env python
"""
Copyright (c) Facebook, Inc. and its affiliates.
All rights reserved.
This source code is licensed under the license found in the LICENSE file in the
root directory of this source tree.

Dataloader for disambiguation task on SIMMC 2.0.

Author(s): Satwik Kottur
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import json

import numpy as np
import torch


class Dataloader:
    def __init__(self, tokenizer, load_path, args, hidden_labels=False):
        self._tokenizer = tokenizer
        self._args = args
        self._hidden_labels = hidden_labels
        print("Loading: {}".format(load_path))
        with open(load_path, "r") as file_id:
            self._raw_data = json.load(file_id)

        self.num_utterances = 2 * args["max_turns"] + 1
        self.num_instances = len(self._raw_data)
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
        for index in indices:
            # Add <USER> and <SYS> tokens.
            dialog_datum = self._raw_data[index]
            dialog = self._raw_data[index]["input_text"]
            for turn_id, turn in enumerate(dialog):
                if turn_id % 2 == 0:
                    dialog[turn_id] = "<USER> " + turn
                else:
                    dialog[turn_id] = "<SYS> " + turn
            text = " ".join(dialog[-self.num_utterances :])
            text_inputs.append(text)
            text_labels.append(dialog_datum["disambiguation_label_gt"])
            dialog_ids.append(dialog_datum["dialog_id"])
            turn_ids.append(dialog_datum["turn_id"])

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
        if self._hidden_labels:
            # Reset all the text_labels to 0.
            text_labels = [0 for ii in text_labels]
        # Pack the batch.
        batch = {
            "text_in": encoded_inputs,
            "gt_label": self.device.LongTensor(text_labels),
            "dialog_id": dialog_ids,
            "turn_id": turn_ids,
        }
        return batch
