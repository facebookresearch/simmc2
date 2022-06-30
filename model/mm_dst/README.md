# SIMMC 2.1 Challenge 2022 (DSTC 11)

This directory contains the code and the scripts for running the baseline models.

The Multimodal Dialog State Tracking (MM-DST) task involves systematically tracking the attributes of dialog act labels cumulative across multiple turns.
Multimodal belief states at each turn should encode sufficient information for handling user utterances in the downstream dialog components (e.g. Dialog Policy).

Please check the [task input](./TASK_INPUTS.md) file for a full description of inputs
for each subtask.

If you would like to use any other external resources, please consult with the track organizers (simmc@fb.com). Generally, we allow the use of publicly available pre-trained language models, such as BERT, GPT-2, etc.

For more details on the task definition and the baseline models we provide, please refer to our SIMMC 2 paper:

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


## Run Baselines

### Baseline: GPT-2 Based DST

1. **Preprocess** the datasets to reformat the data for GPT-2 input.

```
$ cd mm_dst
$ ./run_preprocess_gpt2.sh
```

The shell script above repeats the following for all {train|dev|devtest} splits and both {furniture|fashion} domains.

```
python -m gpt2_dst.scripts.preprocess_input \
    --input_path_json="${PATH_DATA_DIR}"/simmc2.1_dials_dstc11_train.json \
    --output_path_predict="${PATH_DIR}"/gpt2_dst/data/simmc2.1_dials_dstc11_train_predict.txt \
    --output_path_target="${PATH_DIR}"/gpt2_dst/data/simmc2.1_dials_dstc11_train_target.txt \
    --len_context=2 \
    --use_multimodal_contexts=1 \
    --output_path_special_tokens="${PATH_DIR}"/gpt2_dst/data/simmc2_special_tokens.json
```

2. **Train** the baseline model

```
$ ./run_train_gpt2.sh
```

The shell script above repeats the following.

```
$ python -m gpt2_dst.scripts.run_language_modeling \
    --output_dir="${PATH_DIR}"/gpt2_dst/save/model \
    --model_type=gpt2 \
    --model_name_or_path=gpt2 \
    --line_by_line \
    --add_special_tokens="${PATH_DIR}"/gpt2_dst/data/simmc2_special_tokens.json \
    --do_train \
    --train_data_file="${PATH_DIR}"/gpt2_dst/data/simmc2.1_dials_dstc11_train_target.txt \
    --do_eval --eval_all_checkpoints \
    --eval_data_file="${PATH_DIR}"/gpt2_dst/data/simmc2.1_dials_dstc11_dev_target.txt \
    --num_train_epochs=2 \
    --overwrite_output_dir \
    --per_gpu_train_batch_size=4 \
    --per_gpu_eval_batch_size=4
    #--no_cuda
```

3. **Generate** prediction for `devtest` data

```
$ ./run_generate_gpt2.sh
```

The shell script above repeats the following.
```
$ python -m gpt2_dst.scripts.run_generation \
    --model_type=gpt2 \
    --model_name_or_path="${PATH_DIR}"/gpt2_dst/save/model/ \
    --num_return_sequences=1 \
    --length=100 \
    --stop_token='<EOS>' \
    --prompts_from_file="${PATH_DIR}"/gpt2_dst/data/simmc2.1_dials_dstc11_devtest_predict.txt \
    --path_output="${PATH_DIR}"/gpt2_dst/results/simmc2.1_dials_dstc11_devtest_predicted.txt
```

The generation results are saved in the `/mm_dst/results` folder. Change the `path_output` to a desired path accordingly.


4. **Evaluate** predictions for `devtest` data

```
$ ./run_evaluate_gpt2.sh
```

The shell script above runs the following:

```
python -m gpt2_dst.scripts.evaluate \
    --input_path_target="${PATH_DIR}"/gpt2_dst/data/simmc2.1_dials_dstc11_devtest_target.txt \
    --input_path_predicted="${PATH_DIR}"/gpt2_dst/data/simmc2.1_dials_dstc11_devtest_predicted.txt \
    --output_path_report="${PATH_DIR}"/gpt2_dst/results/simmc2.1_dials_dstc11_devtest_report.json
```

Evaluation reports are saved in the `/mm_dst/results` folder as JSON files.

Please note that the GPT2 fine-tuning is highly sensitive to the batch size (which `n_gpu` of your machine may affect), hence it may need some hyperparameter tuning to obtain the best results (and avoid over/under fitting). Please feel free to change the hyperparameter of the default settings (provided) to compare results.

Alternatively, we *also* provide an evaluation script that takes as input a JSON file that is in the same structure as the original data JSON files (in case your model outputs predictions per dialog, as opposed to per turn). For example, the input `pred_dials.json` file should be formatted:

```
{
    "dialogue_data": [
        {
            "dialogue": [
                {
                    "transcript_annotated": [
                          {
                              'act': <str>,
                              'act_attributes': {
                                  "slot_values": {
                                      SLOT_NAME: SLOT_VALUE,
                                      ...
                                  },
                                  "request_slots": [ <str> ],
                                  "objects": [ <int> ],
                                  "disambiguation_candidates": [ <int> ],                                  
                              }
                          },
                          [End of a frame]
                          ...
                    ]
                }
                [End of a turn]
                ...                    
            ],
        },
        [End of a dialogue]
        ...
    ]
}
```


To run this evaluation script:
```
$ ./run_evaluate.sh
```

The shell script above runs the following:

```
python -m utils.evaluate_dst \
    --input_path_target="${PATH_DATA_DIR}"/simmc2.1_dials_dstc11_devtest_dials.json \
    --input_path_predicted="${PATH_DIR}"/simmc2.1_dials_dstc11_devtest_pred_dials.json \
    --output_path_report="${PATH_DIR}"/simmc2.1_dials_dstc11_report.json
```

You can also run response generation without belief states by using the `no_belief_states` flag
while preparing the data.

## Results

Below are the baseline results for the GPT-2 model and Multimodal Transformer Network (MTN) adapted to SIMMC 2.0 ([here][mtn_simmc2]). 

We will soon update the numbers for the new version of the dataset (SIMMC 2.1) and report it here.

**Subtask #2: Multimodal Coreference Resolution**

| Baseline | Object F1 |
| :------: | :-------: |
| GPT2     |   0.366   |
| [MTN-SIMMC2][mtn_simmc2] | - |

**Subtask #3: Multimodal Dialog State Tracking**

| Baseline | Dialog Act F1 | Slot F1 | Request Slot F1 | Joint Accuracy |
| :------: | :-----------: | :-----: | :-------------: | :------------: |
| GPT2     | 0.945         | 0.817   | 0.896           | 0.446          |
| [MTN-SIMMC2][mtn_simmc2] | 0.934 | 0.748 | 0.854     | 0.283          |

**Subtask #4: Multimodal Dialog Response Generation** 

**Generation** 

| Baseline |      BLEU |
| :------: | :-------: |
| GPT2     |   0.192   |
| [MTN-SIMMC2][mtn_simmc2] | 0.217 |


[dstc9]:https://sites.google.com/dstc.community/dstc9/home
[simmc_arxiv]:https://arxiv.org/abs/2006.01460
[simmc2_arxiv]:https://arxiv.org/abs/2104.08667
[mtn_simmc2]:https://github.com/henryhungle/MTN/tree/simmc2
