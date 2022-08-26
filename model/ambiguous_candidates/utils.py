#! /usr/bin/env python
"""
Utility methods for ambiguous candidates identification task

Author(s): Satwik Kottur.
"""

from __future__ import absolute_import, division, print_function, unicode_literals
import argparse
from tqdm import tqdm as progressbar

import torch


def test_non_zero_candidates(loader, label="_unlabelled_"):
    """Count the number of instances with zero target length.

    Args:
        loader: Dataloader used to get the batches
        label: Label to associate for datalaoder, used only to print results.
    """
    batch_size = 10 # any arbitrary batch size.
    num_zero = 0
    num_nonzero = 0
    num_negative = 0
    num_positive = 0
    for batch in progressbar(loader.get_entire_batch(batch_size)):
        num_candidates_batch = [torch.sum(ii) for ii in batch["gt_label"]]
        num_nonzero_batch = sum(ii > 0 for ii in num_candidates_batch)
        num_zero_batch = len(num_candidates_batch) - num_nonzero_batch
        num_zero += num_zero_batch.item()
        num_nonzero += num_nonzero_batch.item()
        num_positive += sum(num_candidates_batch).item()
        num_negative += sum(len(ii) for ii in batch["object_map"])

    percent_zero = num_zero / (num_zero + num_nonzero) * 100
    percent_nonzero = num_nonzero / (num_zero + num_nonzero) * 100
    print(
        f"{label}:\n\t"
        f"# zero [{percent_zero:.1f} %]: {num_zero}\n\t"
        f"# nonzero [{percent_nonzero:.1f} %]: {num_nonzero}"
    )
    percent_positive = num_positive / (num_positive + num_negative) * 100
    percent_negative = num_negative / (num_positive + num_negative) * 100
    print(
        f"{label}:\n\t"
        f"# positive [{percent_positive:.1f} %]: {num_positive}\n\t"
        f"# nonzero [{percent_negative:.1f} %]: {num_negative}"
    )
    return {"label": label, "zeros": num_zero, "nonzeros": num_nonzero}


def compute_precision_recall_f1(n_correct, n_true, n_pred):
    """Computes the precision, recall, and F1 scores.

    Args:
        n_correct: Number of correct (overlapping) predictions
        n_true: Number of ground truth items
        n_pred: Number of items predicted by a model

    Returns:
        rec: Recall
        prec: Precision
        f1: F1 score
    """
    rec = n_correct / n_true if n_true != 0 else 0.
    prec = n_correct / n_pred if n_pred != 0 else 0.
    f1 = 2 * prec * rec / (prec + rec) if (prec + rec) != 0 else 0.
    return rec, prec, f1
