#! /usr/bin/env python
"""
Copyright (c) Facebook, Inc. and its affiliates.
All rights reserved.
This source code is licensed under the license found in the LICENSE file in the
root directory of this source tree.

Implementation of Disambiguation Model.

Author(s): Satwik Kottur
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import argparse

import torch.nn as nn
import transformers


class Disambiguator(nn.Module):
    def __init__(self, tokenizer, args):
        super(Disambiguator, self).__init__()
        self._args = args

        if args["backbone"] == "gpt2":
            self.classifier = (
                transformers.GPT2ForSequenceClassification.from_pretrained(
                    "gpt2", num_labels=2
                )
            )
            self.classifier.config.pad_token_id = self.classifier.config.eos_token_id
        elif args["backbone"] == "bert":
            self.classifier = (
                transformers.BertForSequenceClassification.from_pretrained(
                    "bert-base-uncased", num_labels=2
                )
            )
        else:
            raise NotImplementedError(f"""Invalid backbone: {args["backbone"]}""")
        # Fix model padding token id.
        self.classifier.resize_token_embeddings(len(tokenizer))

        if args["use_gpu"]:
            self.classifier.cuda()

    def forward(self, batch):
        model_out = self.classifier(**batch["text_in"])
        return model_out["logits"]
