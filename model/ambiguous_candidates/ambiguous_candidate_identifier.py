#! /usr/bin/env python
"""
Copyright (c) Facebook, Inc. and its affiliates.
All rights reserved.
This source code is licensed under the license found in the LICENSE file in the
root directory of this source tree.

Implementation of Ambiguous Candidate Identifier Model.

Author(s): Satwik Kottur
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import argparse

import torch
import torch.nn as nn
import transformers


class AmbiguousCandidateIdentifier(nn.Module):
    def __init__(self, tokenizer, args):
        super(AmbiguousCandidateIdentifier, self).__init__()
        self._args = args

        if args["backbone"] == "gpt2":
            self.text_encoder = transformers.GPT2Model.from_pretrained("gpt2")
            self.text_encoder.config.pad_token_id = (
                self.text_encoder.config.eos_token_id
            )
        elif args["backbone"] == "bert":
            self.text_encoder = transformers.BertForTokenClassification.from_pretrained(
                "bert-base-uncased"
            )
        else:
            raise NotImplementedError(f"""Invalid backbone: {args["backbone"]}""")
        # Fix model padding token id.
        self.text_encoder.resize_token_embeddings(len(tokenizer))

        self.text_fc = nn.Linear(
            self.text_encoder.config.hidden_size, args["hidden_size"]
        )
        self.visual_fc = nn.Linear(args["visual_feature_size"], args["hidden_size"])

        if args["use_gpu"]:
            self.text_encoder.cuda()
            self.text_fc.cuda()
            self.visual_fc.cuda()

    def forward(self, batch):
        if self._args["backbone"] == "gpt2":
            model_output = self.text_encoder(
                **batch["text_in"], output_hidden_states=True
            )
            last_hidden_states = model_output[0]
            # Get the hidden state from the last token.
            # Code adopted from:
            # https://huggingface.co/transformers/v3.5.1/_modules/transformers/
            #           modeling_gpt2.html#GPT2ForSequenceClassification
            input_ids = batch["text_in"]["input_ids"]
            batch_size, sequence_length = input_ids.shape
            sequence_lengths = (
                torch.ne(input_ids, self.text_encoder.config.pad_token_id).sum(-1) - 1
            )
            text_embed = last_hidden_states[range(batch_size), sequence_lengths]

        if self._args["backbone"] == "bert":
            model_out = self.text_encoder(**batch["text_in"], output_hidden_states=True)
            last_hidden_states = model_out.hidden_states[-1]
            text_embed = last_hidden_states[:, 0, :]

        text_embed = self.text_fc(text_embed)
        # Compute cosine similarity.
        batch_logits = []
        for visual_feature, text_feature in zip(batch["features"], text_embed):
            visual_embed = self.visual_fc(visual_feature)
            logits = (visual_embed * text_feature).sum(axis=-1)
            batch_logits.append(logits)
        return batch_logits
