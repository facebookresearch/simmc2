#! /usr/bin/env python
"""
Copyright (c) Facebook, Inc. and its affiliates.
All rights reserved.
This source code is licensed under the license found in the LICENSE file in the
root directory of this source tree.

Trains a simple GPT-2 based disambiguation model.

Author(s): Satwik Kottur
"""

from __future__ import absolute_import, division, print_function, unicode_literals
import argparse
import collections
import json
import os

import torch
import torch.nn as nn
from transformers import (
    GPT2Tokenizer,
    get_linear_schedule_with_warmup,
    AdamW,
)
from tqdm import tqdm as progressbar

from dataloader import Dataloader
from disambiguator import Disambiguator


def evaluate_model(model, loader, batch_size, save_path=None):
    num_matches = 0
    results = collections.defaultdict(list)
    with torch.no_grad():
        for batch in progressbar(loader.get_entire_batch(batch_size)):
            output = model(batch)
            predictions = torch.argmax(output, dim=1)
            num_matches += (predictions == batch["gt_label"]).sum().item()

            # Save results if need be.
            if save_path:
                for ii in range(predictions.shape[0]):
                    new_instance = {
                        "turn_id": batch["turn_id"][ii],
                        "disambiguation_label": predictions[ii].cpu().item(),
                    }
                    results[batch["dialog_id"][ii]].append(new_instance)

    # Restructure results JSON and save.
    if save_path:
        results = [
            {"dialog_id": dialog_id, "predictions": predictions,}
            for dialog_id, predictions in results.items()
        ]
        print(f"Saving: {save_path}")
        with open(save_path, "w") as file_id:
            json.dump(results, file_id)

    accuracy = num_matches / loader.num_instances * 100
    return accuracy


def main(args):
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    tokenizer.padding_side = "left"
    # Define PAD Token = EOS Token = 50256
    tokenizer.pad_token = tokenizer.eos_token
    num_added_tokenss = tokenizer.add_special_tokens(
        {"additional_special_tokens": ["<USER>", "SYS>"]}
    )
    # Dataloader.
    train_loader = Dataloader(tokenizer, args["train_file"], args)
    val_loader = Dataloader(tokenizer, args["dev_file"], args)
    test_loader = Dataloader(tokenizer, args["devtest_file"], args)
    # Model.
    model = Disambiguator(tokenizer, args)

    model.train()
    # loss function.
    criterion = nn.CrossEntropyLoss()
    # Prepare optimizer and schedule (linear warmup and decay)
    optimizer = AdamW(
        model.parameters(), lr=args["learning_rate"], eps=args["adam_epsilon"]
    )

    total_steps = (
        int(train_loader.num_instances / args["batch_size"] * args["num_epochs"]) + 1
    )
    num_iters_epoch = train_loader.num_instances // args["batch_size"]
    num_iters = 0
    total_loss = None
    # batch = train_loader.get_random_batch(args["batch_size"])
    while True:
        epoch = num_iters / (float(train_loader.num_instances) / args["batch_size"])

        batch = train_loader.get_random_batch(args["batch_size"])
        output = model(batch)
        loss = criterion(output, batch["gt_label"])

        if total_loss:
            total_loss = 0.95 * total_loss + 0.05 * loss.item()
        else:
            total_loss = loss.item()

        if num_iters % 100 == 0:
            print("[Ep: {:.2f}][Loss: {:.2f}]".format(epoch, total_loss))

        loss.backward()
        optimizer.step()
        model.zero_grad()

        # Evaluate_model every epoch.
        if num_iters % 1000 == 0:
            model.eval()
            accuracy = evaluate_model(model, val_loader, args["batch_size"] * 5)
            print("Accuracy [dev]: {}".format(accuracy))
            # Save devtest results.
            if args["result_save_path"]:
                save_path = os.path.join(
                    args["result_save_path"], f"results_devtest_{num_iters}.json"
                )
            else:
                save_path = None
            accuracy = evaluate_model(
                model, test_loader, args["batch_size"] * 5, save_path
            )
            print("Accuracy [devtest]: {}".format(accuracy))
            model.train()

        num_iters += 1
        if epoch > args["num_epochs"]:
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--train_file", required=True, help="Path to the training file")
    parser.add_argument("--dev_file", required=True, help="Path to the dev file")
    parser.add_argument(
        "--devtest_file", required=True, help="Path to the devtest file"
    )
    parser.add_argument(
        "--result_save_path", default=None, help="Path to save devtest results"
    )
    parser.add_argument(
        "--max_turns", type=int, default=3, help="Number of turns in history"
    )
    parser.add_argument("--batch_size", type=int, default=128, help="Batch Size")
    parser.add_argument(
        "--max_length", type=int, default=512, help="Maximum length in utterance"
    )
    parser.add_argument(
        "--num_epochs", type=int, default=10, help="Maximum number of epochs"
    )
    parser.add_argument(
        "--learning_rate", type=float, default=5e-5, help="Learning rate"
    )
    parser.add_argument(
        "--warmup_steps", type=int, default=0, help="Linear warmup over warmup_steps"
    )
    parser.add_argument(
        "--adam_epsilon", type=float, default=1e-8, help="Eps for Adam optimizer"
    )
    parser.add_argument("--weight_decay", type=float, default=0.0, help="Weight decay")
    parser.add_argument("--use_gpu", dest="use_gpu", action="store_true", default=False)
    try:
        parsed_args = vars(parser.parse_args())
    except (IOError) as msg:
        parser.error(str(msg))
    main(parsed_args)
