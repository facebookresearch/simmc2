# Final Evaluation

Below we describe how the participants can submit their results, and how the winner(s) will be announced.

## Evaluation Dataset

Final evaluation for the SIMMC2.0 DSTC10 track will be on the `test-std` split, different from the `devtest` split. Each test instance in `test-std` contains only `K` number of rounds (not necessarily the entire dialog), where we release the user utterances from `1` to `K` rounds, and system utterances from `1` to `K-1` utterances. Please refer to [this table](./TASK_INPUTS.md) that lists the set of allowed inputs for each subtask.

For subtask 1, evaluation is on disambiguation prediction based on user utterances for the `K`th round.
For subtask 2, evaluation is on coref resolution based on user utterances from `1` through `K`.
For subtask 3, evaluation is on dialog state prediction based on user utterances from `1` through `K`.
For subtask 4, evaluation is on the assistant utterance generation / retrieval for the `K`th round.


## Evaluation Criteria
To be released soon.
