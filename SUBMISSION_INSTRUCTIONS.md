# Final Evaluation

Below we describe how the participants can submit their results, and how the winner(s) will be announced.

## Evaluation Dataset

Final evaluation for the SIMMC2.0 DSTC10 track will be on the `test-std` split, different from the `devtest` split. Use the following files for the final evaluation:
```
data/simmc2_dials_dstc10_teststd_public.json
data/simmc2_dials_dstc10_teststd_retrieval_candidates_public.json
data/simmc2_scene_images_dstc10_teststd.zip
data/simmc2_scene_jsons_dstc10_teststd.zip
```

Each test instance in `test-std` contains only `K` number of rounds (not necessarily the entire dialog), where we release the user utterances from `1` to `K` rounds, and system utterances from `1` to `K-1` utterances. Please refer to [this table](./TASK_INPUTS.md) that lists the set of allowed inputs for each subtask.

For subtask 1, evaluation is on disambiguation prediction based on user utterances for the `K`th round.
For subtask 2, evaluation is on coref resolution based on user utterances from `1` through `K`.
For subtask 3, evaluation is on dialog state prediction based on user utterances from `1` through `K`.
For subtask 4, evaluation is on the assistant utterance generation / retrieval for the `K`th round.

**NOTE**: 
In general, at inference time for a given turn, participants are not allowed to use any of the ground-truth information from its future turns. For instance, for a coreference resolution task at turn `i`, models shouldn't directly make use of the mentioned object IDs from its direct Assistant response turn at `i` or any information from turn `i+1` and on -- which would essentially be regarded as "**peeking into the future**" and thus **unfair/invalid**. 


## Evaluation Criteria

| **Subtask** | **Evaluation** | **Metric Priority List** |
| :-- | :-- | :-- |
| Subtask 1 (Multimodal Disambiguation) | On disambiguation decision for `K`th round | Accuracy |
| Subtask 2 (Multimodal Coreference Resolution) | On coref prediction based on user utterances from 1 through `K` | Object F1 |
| Subtask 3 (Multimodal Dialog State Tracking) | On dialog state based on user utterances from 1 through `K` | Slot F1, Intent F1 |
| Subtask 4 (Multimodal Assistant Response Generation) | On assistant utterance generation for `K`th round | * Generative category: BLEU-4 <br> * Retrieval category: MRR, R@1, R@5, R@10, Mean Rank |

**Separate winners** will be announced for each subtask based on the respective performance, with the exception of subtask 4 (response generation) that will have two winners based on two categories -- generative metrics and retrieval metrics.

Rules to select the winner for each subtask (and categories) are given below:

* For each subtask, we enforce a **priority over the respective metrics** (shown above) to highlight the model behavior desired by this challenge

* The entry with the most favorable (higher or lower) performance on the metric will be labelled as a winner candidate. Further, all other entries within one standard error of this candidate’s performance will also be considered as candidates. If there are more than one candidate according to the metric, we will move to the next metric in the priority list and repeat this process until we have a single winner candidate, which would be declared as the "**subtask winner**".

* In case of multiple candidates even after running through the list of metrics in the priority order, all of them will be declared as "**joint subtask winners**".

**NOTE**:

* Only entries that are able to open-sourced their code will be considered for the final evaluation. In all other cases, we can report the devtest and test-std performances on our result table but cannot declare them as official winners of any subtask.
* **Multiple Submissions:** Similar to other challenges, we are allowing multiple submissions per team if the models' architectures are technically different, or a substantially different training scheme was used to train each model. In these cases, we will evaluate each model independently. If the only difference is, for example, different random seeds, or randomized starting points then we would ask that participants select and submit only one entry for that modeling approach. Overall, we would prefer each team to limit their total number of submissions to say 4 different approaches.



## Submission Format

Participants must submit the model prediction results in JSON format that can be scored with the automatic scripts provided for that sub-task. Specifically, please name your JSON output as follows:

```
<Subtask 1: Multimodal Disambiguation>
dstc10-simmc-teststd-pred-subtask-1.json

<Subtask 2 & 3: Multimodal Co-ref & DST>
dstc10-simmc-teststd-pred-subtask-3.txt (line-separated output)
or
dstc10-simmc-teststd-pred-subtask-3.json (JSON format)

<Subtask 4: >
dstc10-simmc-teststd-pred-subtask-4-generation.json
dstc10-simmc-teststd-pred-subtask-4-retrieval.json
```

The formats are as follows:

```
<Subtask 1>
[
    "dialog_id": <dialog_id>,
    "predictions": [
        {
            "turn_id": <turn_id>,
            "disambiguation_label": <boolean>,
        }
        ...
    ]
    ...
]


<Subtask 2 & 3>
Follow either original data format or line-by-line evaluation.


<Subtask 4 Generation>
[
    "dialog_id": <dialog_id>,
    "predictions": [
        {
            "turn_id": <turn_id>,
            "response": <str; model output>,
        }
        ...
    ]
    ...
]


<Subtask 4 Retrieval>
[
    "dialog_id": <dialog_id>,
    "candidate_scores": [
        {
            "turn_id": <turn_id>,
            "scores": [
                <list of 100 floats>
            ]
        }
        ...
    ]
    ...
]
```

The SIMMC organizers will then evaluate them internally using the following scripts:

```
<Subtask 1>
$ python tools/disambiguator_evaluation.py \
	--pred_file="{PATH_TO_PRED_FILE}" \
	--test_file="{PATH_TO_TEST_FILE}" \

<Subtask 2 & 3>
(line-by-line evaluation)
$ python -m gpt2_dst.scripts.evaluate \
  --input_path_target={PATH_TO_GROUNDTRUTH_TARGET} \
  --input_path_predicted={PATH_TO_MODEL_PREDICTIONS} \
  --output_path_report={PATH_TO_REPORT}

(Or, dialog level evaluation)
$ python -m utils.evaluate_dst \
    --input_path_target={PATH_TO_GROUNDTRUTH_TARGET} \
    --input_path_predicted={PATH_TO_MODEL_PREDICTIONS} \
    --output_path_report={PATH_TO_REPORT}
    
<Subtask 4 Generation>
$ python tools/response_evaluation.py \
    --data_json_path={PATH_TO_GOLD_RESPONSES} \
    --model_response_path={PATH_TO_MODEL_RESPONSES} \
    --single_round_evaluation

<Subtask 4 Retrieval>
$ python tools/retrieval_evaluation.py \
    --retrieval_json_path={PATH_TO_GROUNDTRUTH_RETRIEVAL} \
    --model_score_path={PATH_TO_MODEL_CANDIDATE_SCORES} \
    --single_round_evaluation    
```

**NOTE:** For subtask 1 (multimodal disambiguation), please predict the results
at turns with `disambiguation_label` key.
For `teststd`, we will set this key to `None` to indicate the disambiguation 
turn(s).
The disambiguation turns might not necessarily be the last turns of the provided
dialog file for `teststd`.


## Submission Instructions and Timeline

**UPDATE (Sept 24, 2021)**: Please note that we have changed the deadlines as following:

**NOTE**: All deadlines are 11:59PM UTC-12:00 ("anywhere on Earth"), unless otherwise noted.

<table>
  <tbody>
    <tr>
      <td rowspan=3><ins>Before</ins> Oct 1st, 2021</td>
      <td rowspan=3>Each Team</td>
      <td>Each participating team should create a repository, e.g. in github.com, that can be made public under a permissive open source license (MIT License preferred). Repository doesn’t need to be publicly viewable at that time.</td>
    </tr>
    <tr>
      <td>Before Oct 1st <a href='https://git-scm.com/book/en/v2/Git-Basics-Tagging'>tag a repository commit</a> that contains both runable code and model parameter files that are the team’s entries for all sub-tasks attempted.</td>
    </tr>
    <tr>
      <td>Tag commit with `dstc10-simmc-entry`.</td>
    </tr>
    <tr>
      <td>Oct 1st 2021</td>
      <td>SIMMC Organizers</td>
      <td>Test-Std data released (during US Pacific coast working hours).</td>
    </tr>
    <tr>
      <td rowspan=2><ins>Before</ins> Oct 8th 2021</td>
      <td rowspan=2>Each Team</td>
      <td>Generate test data predictions using the code & the developed model. If there were any changes to the code & model since the Challenge Period 1, tag the new version with `dstc10-simmc-final-entry`.</td>
    </tr>
    <tr>
      <td>For each sub-task attempted, create a PR and check-in to the team’s repository where:
        <ul>
          <li>The PR/check-in contains an output directory with the model output in JSON format that can be scored with the automatic scripts provided for that sub-task.</li>
          <li>The PR comments contain a short technical summary of model.</li>
          <li>Tag the commit with `dstc10-simmc-teststd-pred-subtask-{N}`; where `{N}` is the sub-task number.</li>
        </ul>
      </td>
    </tr>
    <tr>    
      <td rowspan=2><ins>Before</ins> Oct 8th 2021</td>
      <td rowspan=2>Each Team</td>
      <td>Make the team repository public under a permissive Open Source license (e.g. MIT license) to be considered as a (potential) official winner for the SIMMC 2.0 challenge.</td>
    </tr>
    <tr>
      <td>Email the SIMMC Organizers a link to the repository at simmc@fb.com</td>
    </tr>
    <tr>
      <td>Oct 8th - Oct 15th 2021</td>
      <td>SIMMC Organizers</td>
      <td>SIMMC organizers to validate sub-task results.</td>
    </tr>
    <tr>
      <td>By Oct 15th 2021</td>
      <td>SIMMC Organizers</td>
      <td>Publish anonymized team rankings on the SIMMC track github and email each team with their anonymized team identity.</td>
    </tr>
    <tr>
      <td>Post Oct 15th 2021</td>
      <td>SIMMC Organizers</td>
      <td>Our plan is to write up a challenge summary paper. In this we may conduct error analysis of the results and may look to extend, e.g. possibly with human scoring, the submitted results.</td>
    </tr>
  </tbody>
</table>
