
# SIMMC 2.0 Dataset

## Summary

Our challenge focuses on the new SIMMC 2.0 dataset, which is grounded in an immersive virtual environment in the shopping domain: furniture and fashion.

The dataset was collected through the multimodal dialog simulator, followed by a manual paraphrasing step.

The following paper describes in detail the dataset, the collection process, and the annotations we provide:

Satwik Kottur*, Seungwhan Moon*, Alborz Geramifard and Babak Damavandi, ["SIMMC 2.0: A Task-oriented Dialog Dataset for Immersive Multimodal Conversations"](https://arxiv.org/pdf/2104.08667.pdf) (2021).

If you want to publish experimental results with our dataset or use the baseline models, please cite the following article:

```
@article{kottur2021simmc,
  title={SIMMC 2.0: A Task-oriented Dialog Dataset for Immersive Multimodal Conversations},
  author={Kottur, Satwik and Moon, Seungwhan and Geramifard, Alborz and Damavandi, Babak},
  journal={arXiv preprint arXiv:2104.08667},
  year={2021}
}
```

### Dataset Splits

We randomly split each of our SIMMC 2.0 dataset into four components:

| **Split** | **Number of Dialogs** |
| :--: | :--: | 
| Train (64%)   | 7307 | 
| Dev (5%)     | 563 | 
| Test-Dev (15%) | 1687 |
| Test-Std (15%) | 1687 |

**NOTE**
* **Dev** is for hyperparameter selection and other modeling choices.  
* **Test-Dev** is the publicly available test set to measure model performance and report results outside the challenge.  
* **Test-Std** is used as the main test set for evaluation for Challenge Phase 2 (to be released on Sept 24).

## Download the Dataset
We are hosting our datasets in this Github Repository (with [Git LFS](https://git-lfs.github.com/)).
First, install Git LFS
```
$ git lfs install
```

Clone our repository to download both the dataset and the code:
```
$ git clone https://github.com/facebookresearch/simmc2.git
```

## Overview of the Dataset Repository 

The data are made available in the following files:

```
[Main Data]
- Full dialogs: ./simmc2_dials_dstc10_{train|dev|devtest|test}.json
- Scene images: ./simmc2_scene_images_dstc10_public.zip
- Scene JSONs: ./simmc2_scene_jsons_dstc10_public.zip

[Metadata]
- Fashion metadta: ./fashion_prefab_metadata_all.json
- Furniture metadata: ./furniture_prefab_metadata_all.json
```
**NOTE**: The test set will be made available after DSTC10.

## Data Format

For each `{train|dev|devtest}` split, the JSON data is formatted as follows:


```
{
  "split": support.extract_split_from_filename(json_path),
  "version": "simmc2_dstc10",
  "year": 2021,
  "domain": FLAGS.domain,
  "dialogue_data": [
    {
      “dialogue”: [
        {
          “turn_idx”: <int>,      
          “system_transcript”: <str>,
          “system_transcript_annotated”: 
          {
            “act”: <str>,
            "act_attributes": {
              "slot_values": {
                <str> slot_name : <str> slot_value, ...
              },
              "request_slots": [ <str> ],
              "object": [ <int> ]
          },
          “transcript”: <str>,
          “transcript_annotated”: <dict> (same format as above),
          “disambiguation_label”: {0, 1},
        }, // end of a turn (always sorted by turn_idx)
        ...
      ],
      “dialogue_idx”: <int>,    
      “domains”: <str>,    
      “mentioned_object_ids”: [ <int> ],
      "scene_ids": {
        <int> start_turn_id : <str> scene_id
      }
    }
  ] // end of a dialogue
}
```
The scene information file (`{scene_name}_scene.json`) is formatted as follows:

```
{
	"scenes": [
		{
			"objects": [
				{
					"index": <int>, 
					"unique_id": <int>,
					"prefab_path": <str>,
					"bbox": [<int>, <int>, <int>, <int>],
					"position": [<float>, <float>, <float>, <float>],
				}
			],
			"relationships": {
				"<relation>": {
					<obj_id>: <list of objects with relation to obj_id>
				}
			}
		}
	]
}

```

`bbox`: `x`, `y`, `height`, `width` (`x` and `y` are of top left corner of the bounding box)  
Please see `models/utils/visualize_bboxes.py` to better understand these coordinates.   
`position`: Position in the 3D scene, can be ignored for modeling
`index`: Index for the instance in the scene
`unique_id`: Unique index for the instance based on the object


The data can be processed with respective data readers / preprocessing scripts for each sub-task (please refer to the respective README documents). Each sub-task will describe which fields can be used as input.

**NOTES**

`transcript_annotated` provides the detailed structural intents, slots and values for each USER turn. `system_transcript_annotated` provides the similar information for ASSISTANT turns. `object` field in `act_attributes` includes a list of objects referred to in each turn - each marked with a local index throughout the dialog (`obj_idx`).

For instance, a `transcript_annotated` with `act: DA:REQUEST:ADD_TO_CART:CLOTHING` with an object field `[2, 3]` would annotate a user belief state with the intention of adding objects 2 and 3 to the cart.

Participants may use the visual image information for inspection, or as training signals for some of the sub-tasks.

We also release the metadata for each object referred in the dialog data:
```
{
    <int> object_id: {
        “metadata”: {dict},
        “url”: <str> source image
    }, // end of an object
}
```
Attributes for each object either pulled from the original sources or annotated manually. Note that some of the catalog-specific attributes (e.g. availableSizes, brand, etc.) were randomly and synthetically generated. 

Each item in a catalog metadata has a unique `<int> object_id`.
Each `scene_json` defines the mapping from the `local_idx` (local to each dialog), to its canonical `object_id` reference, for each dialog.
This `local_idx` is used in `transcript_annotated` as an object slot.
For example, given a `local_id_to_obj_id_map = {0: 123, 1: 234, 2: 345}` -- the `transcript_annotated`: `{‘act’: ‘DA:REQUEST:ADD_TO_CART’, ‘objects’: [2]}` would indicate this particular dialog act performed upon `OBJECT_2` (`2 == local_idx`), which has a canonical reference to an object with `object_id: 345`.
We are including this information in case you want to refer to the additional information provided in the `metadata.json` file. 
Multimodal disambiguation task is based only on the turns with the 
`disambiguation_label`, either 0 or 1, since it is a binary classification task.
