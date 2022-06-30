# (Archive) The Second Situated Interactive MultiModal Conversations (SIMMC 2.0) Challenge 2021

Welcome to the Second Situated Interactive Multimodal Conversations (SIMMC 2.0) Track page for [DSTC10][dstc10] 2021.

The SIMMC challenge aims to lay the foundations for the real-world assistant agents that can handle multimodal inputs, and perform multimodal actions.
Similar to the [First SIMMC challenge][simmc1] (as part of DSTC9), we focus on the **task-oriented** dialogs that encompass a **situated** multimodal user context in the form of a co-observed & immersive virtual reality (VR) environment.
The conversational context is **dynamically** updated on each turn based on the user actions (e.g. via verbal interactions, navigation within the scene).
For this challenge, we release a new Immersive SIMMC 2.0 dataset in the shopping domains: furniture and fashion.   

The challenge ended successfully in October 2021. The challenge saw a total of 16 model entries from 10 teams across the world (university & industry), setting a new state-of-the-art in 3 subtasks (see the full results and their repositories [here](CHALLENGE_RESULTS.md)).

**Organizers**: Seungwhan Moon, Satwik Kottur, Paul A. Crook, Ahmad Beirami, Babak Damavandi, Alborz Geramifard

<figure>
<img src="./overview.png" width="400" alt="Example from SIMMC" align="center"> 
<figcaption><i>Example from SIMMC-Furniture Dataset</i></figcaption> 
</figure>



### Latest News

* **[Oct 26, 2021]** The official challenge results are announced [here](CHALLENGE_RESULTS.md). The old challenge README page is archived [here](CHALLENGE_README_ARCHIVE.md)
* **[Oct 18, 2021]** The official challenge results were sent to each team. We will soon announce the full results on this GitHub page.
* **[Oct 15, 2021]** The challenge results will be announced by Oct 18 (Mon). Stay tuned!
* **[Oct 1, 2021]** [Test-Std set for the final evaluation](https://github.com/facebookresearch/simmc2/commit/8d23c4879dd873df311b6c49c0674896537b6087) is released. Please follow the [submission instructions carefully](https://github.com/facebookresearch/simmc2/blob/master/SUBMISSION_INSTRUCTIONS.md) and contact us if you have any questions.
* **[Sept 24, 2021]** Submission deadlines have been pushed to accommodate for a [slight change](https://github.com/facebookresearch/simmc2/commit/741e6d32dc354b7c17de7a1b5ec639343f4286d6) in the DST evaluation script. Please see the [Submission Instructions](SUBMISSION_INSTRUCTIONS.md) for more details on the dates.
* **[Sept 14, 2021]** Retrieval candidates for `dev` and `devtest` released.
* **[June 14, 2021]** Challenge announcement. Training / development datasets (SIMMC v2.0) are released.


## Important Links

* [Task Description Paper][simmc2_arxiv] (EMNLP 2021)
* [Data Formats](data/README.md)
* Baseline Details & Results: [Subtask1][subtask1_results], [Subtask 2, 3, 4][subtask2_results]
* [DSTC10 SIMMC 2.0 Results & Models](CHALLENGE_RESULTS.md)
* [DSTC10 SIMMC 2.0 Challenge README (Archive)](CHALLENGE_README_ARCHIVE.md)


## Track Description

### Tasks and Metrics

We present four sub-tasks primarily aimed at replicating human-assistant actions in order to enable rich and interactive shopping scenarios.

| Sub-Task #1 | [Multimodal Disambiguation](model/disambiguate) |
|---------|---------------------------------------------------------------------------------------------------------------------------------------|
| Goal | To classify if the assistant should disambiguate in the next turn |
| Input | Current user utterance, Dialog context, Multimodal context |
| Output |  Binary label |
| Metrics |  Binary classification accuracy |

| Sub-Task #2 | [Multimodal Coreference Resolution](model/mm_dst) |
|---------|---------------------------------------------------------------------------------------------------------------------------------------|
| Goal | To resolve referent objects to thier canonical ID(s) as defined by the catalog. |
| Input | Current user utterance, Dialog context, Multimodal context |
| Output |  Canonical object IDs |
| Metrics |  Coref F1 / Precision / Recall |

| Sub-Task #3 | [Multimodal Dialog State Tracking (MM-DST)](model/mm_dst) |
|---------|---------------------------------------------------------------------------------------------------------------------------------------|
| Goal | To track user belief states across multiple turns |
| Input | Current user utterance, Dialogue context, Multimodal context |
| Output | Belief state for current user utterance |
| Metrics | Slot F1, Intent F1 |

| Sub-Task #4 | [Multimodal Dialog Response Generation & Retrieval](model/mm_dst)  |
|---------|---------------------------------------------------------------------------------------------------------------------------------------|
| Goal | To generate Assistant responses or retrieve from a candidate pool  |
| Input | Current user utterance, Dialog context, Multimodal context, (Ground-truth API Calls) |
| Output | Assistant response utterance |
| Metrics | Generation: BLEU-4, Retrieval: MRR, R@1, R@5, R@10, Mean Rank |


Please check the [task input](./TASK_INPUTS.md) file for a full description of inputs
for each subtask.

### Baseline Results

We provide the baselines for all the four tasks to benchmark their models.
Feel free to use the code to bootstrap your model.

| Subtask | Name | Baseline Results | 
| :--: | :--: | :--: |
| #1 | Multimodal Disambiguation | [Link][subtask1_results] |
| #2 | Multimodal Coreference Resolution | [Link][subtask2_results] |
| #3 | Multimodal Dialog State Tracking (MM-DST) | [Link][subtask3_results] |
| #4 | Multimodal Dialog Response Generation & Retrieval | [Link][subtask4_results] |


## How to Download Datasets and Code

* Git clone our repository to download the datasets and the code. You may use the provided baselines as a starting point to develop your models.
```
$ git lfs install
$ git clone https://github.com/facebookresearch/simmc2.git
```

* Also please feel free to check out other open-sourced repositories for the SIMMC 2.0 challenge [here](CHALLENGE_RESULTS.md).
 

## Contact

### Questions related to SIMMC Track, Data, and Baselines
Please contact simmc@fb.com, or leave comments in the Github repository.

### DSTC Mailing List
If you want to get the latest updates about DSTC10, join the [DSTC mailing list](https://groups.google.com/a/dstc.community/forum/#!forum/list/join).


## Citations

If you want to publish experimental results with our datasets or use the baseline models, please cite the following articles:

```
@inproceedings{kottur-etal-2021-simmc,
    title = "{SIMMC} 2.0: A Task-oriented Dialog Dataset for Immersive Multimodal Conversations",
    author = "Kottur, Satwik  and
      Moon, Seungwhan  and
      Geramifard, Alborz  and
      Damavandi, Babak",
    booktitle = "Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing",
    month = nov,
    year = "2021",
    address = "Online and Punta Cana, Dominican Republic",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2021.emnlp-main.401",
    doi = "10.18653/v1/2021.emnlp-main.401",
    pages = "4903--4912",
}
```
**NOTE**: The [paper][simmc2_arxiv] (EMNLP 2021) above describes in detail the datasets, the collection process, and some of the baselines we provide in this challenge. 

## License

SIMMC 2.0 is released under [CC-BY-NC-SA-4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode), see [LICENSE](LICENSE) for details.


[dstc10]:https://sites.google.com/dstc.community/dstc10/home
[simmc1]:https://github.com/facebookresearch/simmc
[simmc2_arxiv]:https://arxiv.org/pdf/2104.08667.pdf
[simmc_arxiv]:https://arxiv.org/abs/2006.01460
[subtask1_results]:./model/disambiguate#performance-on-simmc-20
[subtask2_results]:./model/mm_dst#results
[subtask3_results]:./model/mm_dst#results
[subtask4_results]:./model/mm_dst#results
