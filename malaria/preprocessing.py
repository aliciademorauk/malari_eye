import pandas as pd
import json

# importing bounding box (BB) JSON file and preparing the dataframe so that all the leukocytes
# are removed, and the BBs are filtered to eliminate too large and not square enough

with open('../malaria_data/training.json') as f:
    data = json.load(f)

# create empty dictionary with column names as keys
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

# run a first for loop to get each image from list
for image in data:

#     run a nested loop withing each image to get the individual object data

    #Populate cells_df dict with bounding box data
    for box in image['objects']:
        cells_df['path'].append(image['image']['pathname'])
        cells_df['min_r'].append(box['bounding_box']['minimum']['r'])
        cells_df['min_c'].append(box['bounding_box']['minimum']['c'])
        cells_df['max_r'].append(box['bounding_box']['maximum']['r'])
        cells_df['max_c'].append(box['bounding_box']['maximum']['c'])
        cells_df['r_len'].append(box['bounding_box']['maximum']['r']-box['bounding_box']['minimum']['r'])
        cells_df['c_len'].append(box['bounding_box']['maximum']['c']-box['bounding_box']['minimum']['c'])
        cells_df['category'].append(box['category'])

# create dataframe using pandas (80113 rows)

training_json_df = pd.DataFrame(cells_df)

# create size analysis columns (80113 rows)

training_json_df['box_area'] = training_json_df['c_len']*training_json_df['r_len']
training_json_df['c_by_r'] = training_json_df['c_len']/training_json_df['r_len']
training_json_df['r_by_c'] = training_json_df['r_len']/training_json_df['c_len']

# filtering dataframe eliminating too rectangle-y bounding boxes (70942 left)

square_enough = training_json_df.query('0.75 <= r_by_c <= 1.25 and 0.75 <= c_by_r <= 1.25')
square_enough

# filtering out very large bounding boxes (70828 left)

square_enough_and_good_size = square_enough.query('box_area <= 25000')
square_enough_and_good_size

# removing labelled leukocytes

square_enough_good_size_no_leukocytes = square_enough_and_good_size.drop(
    square_enough_and_good_size[square_enough_and_good_size['category'] == 'leukocyte'].index)
square_enough_good_size_no_leukocytes
