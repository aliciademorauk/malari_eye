import pandas as pd
import numpy as np
import json
import os

# instantiate the coco dictionary format with the empty images and annotations lists

coco_json = {
    "info": {
        "year": "2020",
        "version": "1",
        "description": "Exported from roboflow.ai",
        "contributor": "",
        "url": "https://app.roboflow.ai/datasets/bccd-single-image-example/1",
        "date_created": "2020-01-30T23:05:21+00:00"
    },
    "licenses": [
        {
            "id": 1,
            "url": "",
            "name": "Unknown"
        }
    ],
    "categories": [
        {
            "id": 0,
            "name": "difficult",
            "supercategory": "none"
        },
        {
            "id": 1,
            "name": "gametocyte",
            "supercategory": "cells"
        },
        {
            "id": 2,
            "name": "leukocyte",
            "supercategory": "cells"
        },
        {
            "id": 3,
            "name": "red blood cell",
            "supercategory": "cells"
        },
        {
            "id": 4,
            "name": "ring",
            "supercategory": "cells"
        },
        {
            "id": 5,
            "name": "schizont",
            "supercategory": "cells"
        },
        {
            "id": 6,
            "name": "trophozoite",
            "supercategory": "cells"
        }
    ],
    "images": [],
    "annotations": []
}

# open the training json
dir=os.path.dirname(os.path.dirname(__file__))
path = os.path.join(dir,'malaria_data','test.json')
with open(path) as f:
    data = json.load(f)
# create separate image and cells dictionaries
image_df = {
    'path':[],
    'shape_r':[],
    'shape_c':[],
    'channels':[]
}
cells_df = {
    'path':[],
    'min_r':[],
    'min_c':[],
    'max_r':[],
    'max_c':[],
    'r_len':[],
    'c_len':[],
    'category':[]
}

for image in data:
    #Populate image_df dict
    image_df['path'].append(image['image']['pathname'])
    image_df['shape_r'].append(image['image']['shape']['r'])
    image_df['shape_c'].append(image['image']['shape']['c'])
    image_df['channels'].append(image['image']['shape']['channels'])

    #Populate cells_df dict
    for box in image['objects']:
        cells_df['path'].append(image['image']['pathname'])
        cells_df['min_r'].append(box['bounding_box']['minimum']['r'])
        cells_df['min_c'].append(box['bounding_box']['minimum']['c'])
        cells_df['max_r'].append(box['bounding_box']['maximum']['r'])
        cells_df['max_c'].append(box['bounding_box']['maximum']['c'])
        cells_df['r_len'].append(box['bounding_box']['maximum']['r']-box['bounding_box']['minimum']['r'])
        cells_df['c_len'].append(box['bounding_box']['maximum']['c']-box['bounding_box']['minimum']['c'])
        cells_df['category'].append(box['category'])

#transform populated dicts into DFs
image_df = pd.DataFrame(image_df)
cells_df = pd.DataFrame(cells_df)

# create a dictionary to transpose string categories into int categories
cat_dict = {cat: i for i, cat in enumerate(np.unique(cells_df['category']))}

# doublé for loop appending the images and annotations empty lists within the dict
for index, image in enumerate(image_df['path']):
        coco_json['images'].append({
            "id": index,
            "license": 1,
            "file_name": image.split('/')[-1],
            "height": 1200,
            "width": 1600,
            "date_captured": "2020-02-02T23:05:21+00:00"
        })
        for index_2, row in cells_df[cells_df['path']==image].iterrows():
            coco_json['annotations'].append({
                "id": index_2,
                "image_id": index,
                "category_id": cat_dict[row['category']],
                "bbox": [
                    row['min_c'],
                    row['min_r'],
                    row['c_len'],
                    row['r_len']
                ],
                "area": row['r_len']*row['c_len'],
                "segmentation": [],
                "iscrowd": 0
            })

# Open a file and write the data to it
with open('test_coco.json', 'w') as f:
    json.dump(coco_json, f)
