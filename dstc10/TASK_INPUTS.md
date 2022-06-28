**Allowed Inputs**

* The guideline below shows the input fields that are allowed (default) and disallowed (marked as 'X') at **inference time**, for each subtask.
* Participants are free to use any of the fields below during **training** though as additional supervision signals, and *e.g.* at the inference time use the reconstructed / predicted values instead.

**NOTE**: In general, at inference time for a given turn, participants are not allowed to use any of the ground-truth information from its future turns. For instance, for a coreference resolution task at turn `i`, models shouldn't directly make use of the mentioned object IDs from its direct Assistant response turn at `i` or any information from turn `i+1` and on -- which would essentially be regarded as "peeking into the future" and thus unfair/invalid. 


| Key |  Subtask #1 </br>(Multimodal Disambiguation) | Subtask #2 <br>(Multimodal Coreference Resolution) | Subtask #3 <br> (MM-DST) | Subtask #4 <br> (Response Generation) | 
|:---|:---:|:---:|:---:|:---:|
|**Dialog JSON File (Turn Level Input Fields)**| | | |
|`system_transcript`<br>(previous turns)|  |  |  |
|`system_transcript`<br>(current turn) | ✗ | ✗ | ✗ |  ✗<br>(prediction target) |
|`system_transcript_annotated`<br>(previous turns)| ✗<br>(except mentioned object IDs) | ✗<br>(except mentioned object IDs) | ✗<br>(except mentioned object IDs) | ✗ |
|`system_transcript_annotated`<br>(current turn)| ✗ | ✗ | ✗ |  |
|`transcript`| | |  |
|`transcript_annotated` | ✗<br>(prediction target) | ✗<br>(prediction target) | ✗<br>(prediction target) | ✗ |
|`turn_idx`| | | |
|`disambiguation_label`| ✗ | ✗ | ✗ | ✗ |
|`scene_ids`|
|**Dialog JSON File (Dialog Level Input Fields)**| | | |
|`mentioned_object_ids` (* defined at a dialog level)| ✗ | ✗ | ✗ | ✗ |
| `dialogue_idx` | 
|  `domain` | 
|**Scene JSON Files**| | | |
|`objects` (index, bbox, ...)| | | |
|`relationships`| | | |
|**Prefab Metadata Files**| | | |
|`url` (raw image)| | | |
|Non-visual Metadata<br>(`customerReview`,`brand`,`price`,`size`,`materials`)|  
|Visual Metadata<br>(`assetType`,`color`,`pattern`,`sleeveLength`,`type`) | ✗ | ✗ | ✗ | ✗ |

**Notes**

`transcript_annotated` provides the detailed structural intents, slots and values for each USER turn. `system_transcript_annotated` provides the similar information for ASSISTANT turns.

`object` field in `transcript_annotated` includes a list of object IDs referred to in each turn - each marked with a local index as defined for each scene.

For more details, please refer to the full description in the [data README document](https://github.com/facebookresearch/simmc2/tree/master/data).
