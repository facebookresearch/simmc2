#! /usr/bin/env python
"""Copyright (c) Facebook, Inc. and its affiliates.
All rights reserved.
This source code is licensed under the license found in the LICENSE file in the
root directory of this source tree.

Visualizes bounding boxes from SCENE JSON files for SIMMC 2.0.

Author(s): Satwik Kottur
"""

from __future__ import absolute_import, division, print_function, unicode_literals
import argparse
import collections
import json
import sys
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from tqdm import tqdm as progressbar


def draw_bboxes(bboxes, load_path, save_path, verbose=False):
    """Draw bounding boxes given the screenpath and list of bboxes.

    Args:
        bboxes: List of all bounding boxes
        load_path: Path to load the screenshot
        save_path: Path to save the screenshot with bounding boxes
        verbose: Print out status statements
    """
    # Read images and draw rectangles.
    image = Image.open(load_path)
    draw = ImageDraw.Draw(image)
    # Get a font.
    font = ImageFont.load_default()
    # font = ImageFont.truetype("arial.ttf", size=20)
    offset = 2
    for index, bbox_datum in enumerate(bboxes):
        object_index = bbox_datum.get("index", index)
        verts = bbox_datum["bbox"]
        draw.rectangle(
            [(verts[0], verts[1]), (verts[0] + verts[3], verts[1] + verts[2])]
        )
        # Draw text with black background.
        text = str(object_index)
        text_width, text_height = font.getsize(text)
        draw.rectangle(
            (
                verts[0] + offset,
                verts[1] + offset,
                verts[0] + 2 * offset + text_width,
                verts[1] + 2 * offset + text_height,
            ),
            fill="black",
        )
        draw.text(
            (verts[0] + offset, verts[1] + offset),
            str(object_index),  # str(index)
            fill=(255, 255, 255),
            font=font,
        )
    # Save the image with bbox drawn.
    if verbose:
        print("Saving: {}".format(save_path))
    image.save(save_path, "PNG")


def get_screenshot_save_path(screenshot_path):
    file_name, extension = screenshot_path.rsplit(".", 1)
    return "{}_bbox_draw.{}".format(file_name, extension)


def main(args):
    if args["scene_names"] == "all":
        # Get all the scene names in the folder.
        scene_names = [
            ii.rsplit("_", 1)[0] for ii in os.listdir(args["scene_json_root"])
        ]
        scene_names = list(set(scene_names))
        # Remove explore.py.
        scene_names.remove("explore.py")
    else:
        scene_names = args["scene_names"]

    print(f"""Reading scene JSONS: {args["scene_json_root"]}""")
    print(f"""Reading scene screenshots: {args["screenshot_root"]}""")
    for scene in progressbar(scene_names):
        json_path = os.path.join(args["scene_json_root"], f"{scene}_scene.json")
        # Check if file exists, else try with "m_"
        if not os.path.exists(json_path):
            json_path = os.path.join(args["scene_json_root"], f"m_{scene}_scene.json")
            assert os.path.exists(json_path), f"{json_path} not found!"
        with open(json_path, "r") as file_id:
            scene_json = json.load(file_id)
        object_bboxes = scene_json["scenes"][0]["objects"]

        # Image load and save paths.
        trimmed_scene_name = scene[2:] if scene[:2] == "m_" else scene
        screenshot_load_path = os.path.join(
            args["screenshot_root"], f"{trimmed_scene_name}.png"
        )
        screenshot_save_path = os.path.join(
            args["save_root"], f"{trimmed_scene_name}_bbox.png"
        )
        draw_bboxes(object_bboxes, screenshot_load_path, screenshot_save_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--screenshot_root", required=True, help="Folder with scene screenshots"
    )
    parser.add_argument(
        "--scene_json_root", default=None, help="Folder with scene JSONs"
    )
    parser.add_argument(
        "--save_root", default=None, help="Folder to save the screenshots w/ bboxes"
    )
    parser.add_argument(
        "--scene_names",
        nargs="+",
        default="all",
        help="List of scenes to visualize, or all",
    )
    try:
        parsed_args = vars(parser.parse_args())
    except (IOError) as msg:
        parser.error(str(msg))
    main(parsed_args)
