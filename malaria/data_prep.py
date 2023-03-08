import pandas as pd
import json
import numpy as np
from PIL import Image
import os

# importing bounding box (BB) JSON file and preparing the dataframe so that all the leukocytes
# are removed, and the BBs are filtered to eliminate too large and not square enough

print(os.getcwd())
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

# # removing labelled leukocytes - NB Removed from code for now

# square_enough_good_size_no_leukocytes = square_enough_and_good_size.drop(
#     square_enough_and_good_size[square_enough_and_good_size['category'] == 'leukocyte'].index)
# square_enough_good_size_no_leukocytes

# import the function to splice, grayscale and resize the cells

def return_resized_cell_array(iter_df, n_cells=0):
# enter the name of the dataframe and the number of cells if not whole dataframe
# create two lists, which will become our X and ys
    spliced_cells = []
    spliced_cells_category = []
    #  if function has value that isn't zero bypass statement
    if n_cells != 0:
        iter_df = iter_df.head(n_cells)
    #     for loop going row by row in dataset
    for index, row in iter_df.iterrows():
    #     rename the min and max r and cs
        x1 = iter_df['min_r'][index]
        x2 = iter_df['max_r'][index]
        y1 = iter_df['min_c'][index]
        y2 = iter_df['max_c'][index]
    #        create f string from path column to open each large image in np.array using Pillow image package
        image = np.array(Image.open(f'../malaria_data{iter_df["path"][index]}'))
    #        convert np.array into grayscale using Pillow image package
        grayscale_image = Image.fromarray(image).convert('L')
    #         convert grayscale image back into np.array
        grayscale_array = np.array(grayscale_image)
    #     splice the np.array using the 4 coordinates
        bounding_box = grayscale_array[ x1 : x2 , y1 : y2 ]
    #        resize the bounding box to universalise to 108 by 108
        bounding_box_resize = Image.fromarray(bounding_box).resize((108,108), resample=0)
    #        append to both lists
        spliced_cells.append(np.array(bounding_box_resize))
        spliced_cells_category.append(iter_df['category'][index])

    #        make numpy files
    np.save('x_values.npy', np.array(spliced_cells))
    np.save('y_values.npy', np.array(spliced_cells_category))

    return spliced_cells, spliced_cells_category

# call the function on the relevant dataframe (for now square_enough_and_good_size)
# for now we're limiting the number of cells called to 1000

return_resized_cell_array(square_enough_and_good_size, n_cells=1000)
