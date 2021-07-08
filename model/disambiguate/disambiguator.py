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

from transformers import GPT2Config, GPT2ForSequenceClassification
import torch.nn as nn


class Disambiguator(nn.Module):
    def __init__(self, tokenizer, args):
        super(Disambiguator, self).__init__()
        model_config = GPT2Config.from_pretrained(
            pretrained_model_name_or_path="gpt2", num_labels=2
        )
        self.lm = GPT2ForSequenceClassification(model_config)
        # Fix model padding token id.
        self.lm.resize_token_embeddings(len(tokenizer))
        self.lm.config.pad_token_id = self.lm.config.eos_token_id

        if args["use_gpu"]:
            self.lm.cuda()

    def forward(self, batch):
        model_out = self.lm(**batch["text_in"])
        return model_out["logits"]
