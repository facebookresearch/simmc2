# SIMMC 2.0 Challenge 2021 | Sub-Task #1: Multimodal Disambiguation


This directory contains the code and the scripts for running the baseline model for Sub-Task #1: Multimodal Disambiguation.

The multimodal disambiguation task involves identifying whether a given user turn contains ambiguity and thus requires disambiguation in the subsequent assistant turn.

Please check the [task input](./TASK_INPUTS.md) file for a full description of inputs for each subtask.

For more details on the task definition and the baseline models we provide, please refer to our SIMMC paper:

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


1. **Preprocess** the datasets to reformat the data for GPT-2 input.

```
$ python format_disambiguation_data.py \
	--simmc_train_json="../../data/simmc2_dials_dstc10_train.json" \
	--simmc_dev_json="../../data/simmc2_dials_dstc10_dev.json" \
	--simmc_devtest_json="../../data/simmc2_dials_dstc10_devtest.json" \
	--disambiguate_save_path="../../data/"
```

2. **Train** and simultaneously test the baseline model.

```
$ python train_model.py \
	--train_file="../../data/simmc2_disambiguate_dstc10_train.json" \
	--dev_file="../../data/simmc2_disambiguate_dstc10_dev.json" \
	--devtest_file="../../data/simmc2_disambiguate_dstc10_devtest.json" \
    --result_save_path="results/" \
	--use_gpu --batch_size=8 --learning_rate=2e-5 --max_turns=5
```

## Performance on SIMMC 2.0
**Note**: We pick the model with best `dev` performance and report the corresponding `testdev` performance.

| Baseline | Accuracy |
| :------: | :------: |
| GPT2-Disambiguator | 73.9 |


[dstc9]:https://sites.google.com/dstc.community/dstc9/home
[simmc2_arxiv]:https://arxiv.org/abs/2104.08667
