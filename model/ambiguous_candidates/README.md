# SIMMC 2.1 Challenge 2022 | Sub-Task #1: Ambiguous Candidate Identification


This directory contains the code and the scripts for running the baseline model
for Sub-Task #1: Ambiguous Candidate Identification.

The ambiguous candidate identification task focuses on identifying the set of items in the scene that
are candidates for an ambiguous user turn, given the dialog context and the multimodal scene information.
This reasoning step is useful for a multimodal conversational AI assistant to tend decide its strategy
for disambiguation in subsequent turns.

Please check the [task input](./TASK_INPUTS.md) file for a full description of inputs for each subtask.

Since this is a new task introduced in the SIMMC 2.1 challenge (2022), please refer to the [proposal][simmc2.1_proposal] for further details on this task.
For prior task definitions and the baseline models, please refer to our SIMMC paper:

```
@article{kottur2021simmc,
  title={SIMMC 2.0: A Task-oriented Dialog Dataset for Immersive Multimodal Conversations},
  author={Kottur, Satwik and Moon, Seungwhan and Geramifard, Alborz and Damavandi, Babak},
  journal={arXiv preprint arXiv:2104.08667},
  year={2021}
}
```
**NOTE**: The [paper][simmc2_arxiv] reports the results from an earlier version of the dataset and with different train-dev-test splits, hence the baseline performances on the challenge resources will be slightly different.


## Installation (Same across all sub-tasks)

* Git clone the repository:
```
$ git lfs install
$ git clone https://github.com/facebookresearch/simmc.git
```

* Install the required Python packages:
  * [Python 3.6+](https://www.python.org/downloads/)
  * [PyTorch 1.5+](https://pytorch.org/get-started/locally/#start-locally)
  * [Transformers](https://huggingface.co/transformers/installation.html)

**NOTE**: We recommend installation in a virtual environment ([user guide](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)). Create a new virtual environment and activate it prior to installing the packages.


## Run Baseline

Step 1: **Preprocess** the SIMMC 2.1 dataset to reformat the data for a friendlier format towards ambiguous candidate identification.  

```
$ DATA_FOLDER="../../data/"
$ python format_ambiguous_candidates_data.py \
	--simmc_train_json "../../data/simmc2.1_dials_dstc11_train.json" \
	--simmc_dev_json "../../data/simmc2.1_dials_dstc11_dev.json" \
	--simmc_devtest_json "../../data/simmc2.1_dials_dstc11_devtest.json" \
	--scene_json_folder "../../data/public/" \
	--ambiguous_candidates_save_path "../../data/ambiguous_candidates/"
```
Here, `scene_json_folder` refers to the folder containing scene JSON files after unziping `simmc2_scene_jsons_dstc10_public.zip`.


Step 2: **Train** and simultaneously test the baseline model with either `bert` or `gpt2` backbones.

```
$ python train_model.py \
    --train_file "../../data/simmc2.1_ambiguous_candidates_dstc11_train.json" \
    --dev_file "../../data/simmc2.1_ambiguous_candidates_dstc11_dev.json" \
    --devtest_file "../../data/simmc2.1_ambiguous_candidates_dstc11_devtest.json" \
    --result_save_path "results/" \
    --visual_feature_path "../../data/visual_features_resnet50_simmc2.1.pt" \
    --visual_feature_size 516 \
	--backbone bert --use_gpu --num_epochs 10 --batch_size 16 --max_turns 2
```
Visual features have been extracted using ResNet-50 backbone for the corresponding bounding boxes.
You can download pre-extracted visual features `visual_feature_path` [here][simmc2.1_visual_features]
(`visual_feature_size` is 516-d = 512-d ResNet-50 features + 4-d normalized bounding box features).

## Performance on SIMMC 2.1
**Note**: We pick the model with best `dev` F1 performance and report the corresponding `testdev` performance.
In addition to the baselines with `bert` and `gpt2` backbones, we also experiment with heuristic baselines like selecting no object, all objects, or random objects.

|    Baseline    | Recall | Precision |    F1    |
| :------------: | :----: | :-------: | :------: | 
| No Object      |   0.0  |    0.0    |    0.0   |
| Random Objects |  48.7  |   22.0    |   30.3   |
| All Objects    |  100.0 |   22.3    |   36.5   |
| GPT-2          |  80.9  |   29.5    |   43.2   |
| BERT           |  73.5  |   31.3    |   43.9   |


[dstc9]:https://sites.google.com/dstc.community/dstc9/home
[simmc2_arxiv]:https://arxiv.org/abs/2104.08667
[simmc2.1_proposal]:https://drive.google.com/file/d/1_Tdl7CXm71gqlWutbOe0e8O1hhiycsQf/view
[simmc2.1_visual_features]:https://drive.google.com/file/d/1jr7r5Yaca80W5n0hizOakTG-F1ns6BGv/view?usp=sharing
