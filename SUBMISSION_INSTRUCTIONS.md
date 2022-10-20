# Final Evaluation

Below we describe how the participants can submit their results, and how the winner(s) will be announced.

## Evaluation Dataset

Final evaluation for the SIMMC2.1 DSTC11 track will be on the `test-std` split, different from the `devtest` split. 
We will release the `test-std` split closer to the end of Challenge Period 1 (Oct 21). Please check this page again later for more details.


**NOTE**:

* Only entries that are able to open-sourced their code will be considered as the challenge winners in the final evaluation. In all other cases, we can report the devtest and test-std performances on our result table & report paper, but cannot declare them as official winners of any subtask.
* **Multiple Submissions:** Similar to other challenges, we are allowing multiple submissions per team if the models' architectures are technically different, or a substantially different training scheme was used to train each model. In these cases, we will evaluate each model independently. If the only difference is, for example, different random seeds, or randomized starting points then we would ask that participants select and submit only one entry for that modeling approach.


## Submission Format

Participants must submit the model prediction results in JSON format that can be scored with the automatic scripts provided for that sub-task. Specifically, please name your JSON output as follows:


```
<Subtask 1, 2 & 3>
dstc11-simmc-teststd-pred-subtask-123.txt (line-separated output)
or
dstc11-simmc-teststd-pred-subtask-123.json (JSON format)

<Subtask 4: >
dstc10-simmc-teststd-pred-subtask-4.json
```

The formats are as follows:

```
<Subtask 1, 2, 3>
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
```

The SIMMC organizers will then evaluate them internally using the following scripts:

```
<Subtask 1, 2, 3>

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
```

## Submission Instructions and Timeline

**NOTE**: All deadlines are 11:59PM UTC-12:00 ("anywhere on Earth"), unless otherwise noted.

<table>
  <tbody>
    <tr>
      <td rowspan=4><ins>Before</ins> Oct 21, 2022</td>
      <td rowspan=4>Each Team</td>
      <td>Each participating team should create a repository, e.g. in github.com, that can be made public under a permissive open source license (MIT License preferred). Repository doesn’t need to be publicly viewable at that time.</td>
    </tr>
    <tr>
        <td>
        In the main README.md file of your repository, please indicate the model performances on the devtest set (= output of the evaluation scripts).
        </td>
    </tr>
    <tr>
      <td>
          Before Oct 21 <a href='https://git-scm.com/book/en/v2/Git-Basics-Tagging'>tag a repository commit</a> that contains both runable code and model parameter files that are the team’s entries for all sub-tasks attempted.
          <br>
          * Note: This (soft) deadline is just to help participants better prepare for the final teststd submission. Minor code changes and model improvements are still allowed after this time.
      </td>
    </tr>
    <tr>
      <td>Tag commit with `dstc11-simmc-entry`.</td>
    </tr>
    <tr>
      <td>Oct 21, 2022</td>
      <td>SIMMC Organizers</td>
      <td>Test-Std data released (during US Pacific coast working hours).</td>
    </tr>
    <tr>
      <td rowspan=2><ins>Before</ins> Oct 28, 2022</td>
      <td rowspan=2>Each Team</td>
      <td>Generate test data predictions using the code & the developed model. If there were any changes to the code & model since the Challenge Period 1, tag the new version with `dstc11-simmc-final-entry`.</td>
    </tr>
    <tr>
      <td>For each sub-task attempted, create a PR and check-in to the team’s repository where:
        <ul>
          <li>The PR/check-in contains an output directory with the model output in JSON format that can be scored with the automatic scripts provided for that sub-task.</li>
          <li>The PR comments contain a short technical summary of model.</li>
          <li>Tag the commit with `dstc11-simmc-teststd-pred-subtask-{N}`; where `{N}` is the sub-task number.</li>
        </ul>
      </td>
    </tr>
    <tr>    
      <td rowspan=2><ins>Before</ins> Oct 28, 2022</td>
      <td rowspan=2>Each Team</td>
      <td>Make the team repository public under a permissive Open Source license (e.g. MIT license) to be considered as a (potential) official winner for the SIMMC 2.1 challenge.</td>
    </tr>
    <tr>
      <td>Email the SIMMC Organizers a link to the repository at simmc@fb.com</td>
    </tr>
    <tr>
      <td>Oct 28 - Early November, 2022</td>
      <td>SIMMC Organizers</td>
      <td>SIMMC organizers to validate sub-task results.</td>
    </tr>
    <tr>
      <td>Early November, 2022</td>
      <td>SIMMC Organizers</td>
      <td>Publish anonymized team rankings on the SIMMC track github and email each team with their anonymized team identity.</td>
    </tr>
    <tr>
      <td>Post November, 2022 </td>
      <td>SIMMC Organizers</td>
      <td>Our plan is to write up a challenge summary paper. In this we may conduct error analysis of the results and may look to extend, e.g. possibly with human scoring, the submitted results.</td>
    </tr>
  </tbody>
</table>
