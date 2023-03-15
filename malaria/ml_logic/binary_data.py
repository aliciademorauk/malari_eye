import pandas as pd
import json
import numpy as np
from PIL import Image
import os
# from malaria.params import *


''' Import JSON file which has bounding box (BB) coordinates and cell types for a Slide Image.
There are many BB on each slide (c. 50-80)
Prepare a dataframe which has the url to the Slide Image photo, and the BB coordinates of each cell and cell type

[**not implemented here
Remove all:
    leukocytes,
    difficult (categorisation of unclear cells)]

Filter records to remove very large BB, and also any rectangular ones (>3/4 dims)
Return two arrays of X, y of selected data

'''

IMG_OUTPUT_SIZE = (200,200) # this is the size we have settled on as the mean
BOX_AREA = np.product(IMG_OUTPUT_SIZE) * 2.5 # make the max box size acceptable 2.5 x 108 x 108
R_BY_C = 3/4

base_filepath_to_json_images = os.path.join("malaria_data")
base_filepath_train_test = os.path.join("malaria","train_test_data")

df = pd.read_csv('../malaria_data/RBC20k_no_diff_leuk.csv')
df['category'] = df['category'].replace({
    'red blood cell': 'uninfected',
    'trophozoite': 'infected',
    'ring': 'infected',
    'gametocyte': 'infected',
    'schizont': 'infected'
})
iter_df = df[df['category'] != 'leukocyte']

def return_resized_cell_array(iter_df, im_col, n_cells):
# enter the name of the dataframe and the number of cells if not whole dataframe
# create two lists, which will become our X and ys
    spliced_cells = []
    spliced_cells_category = []
    #  if function has value that isn't zero bypass statement
    if n_cells != 0:
        iter_df = iter_df.head(n_cells)

    #     for loop going row by row in dataset

    for index, row in iter_df.iterrows():
        if index == 0:
            img = get_img(base_filepath_to_json_images,
                          iter_df.loc[index,"path"],
                          im_col)
        else:
            if (row.path != prior_row_path):
                img = get_img(base_filepath_to_json_images,
                              row.path,
                              im_col)

    #     rename the min and max r and cs
        y1 = iter_df['min_r'][index]
        y2 = iter_df['max_r'][index]
        x1 = iter_df['min_c'][index]
        x2 = iter_df['max_c'][index]

    #   crop the image using the 4 coordinates
        bounding_box = img.crop((x1, y1, x2, y2))
    #   resize the bounding box to universalise to 108 by 108

        bounding_box_resize = bounding_box.resize(IMG_OUTPUT_SIZE, resample=0)

    #   append to both lists
        spliced_cells.append(np.array(bounding_box_resize))
        spliced_cells_category.append(iter_df['category'][index])

        prior_row_path = row.path

    return spliced_cells, spliced_cells_category

# call the function on the relevant dataframe (for now square_enough_and_good_size)
# for now we're limiting the number of cells called to 1000

def get_img(base_filepath_to_json_images, img_path, im_col):
    #create f string from path column to open each large image in np.array using Pillow image package
    # breakpoint()
    img = Image.open(f"{base_filepath_to_json_images}{img_path}")
    #
    if im_col:
        PIL_type = 'RGB'
        img = img.convert(PIL_type)
    else:
        PIL_type = 'L'
        img = img.convert(PIL_type)

    return img


def process_save_array(source_filename, im_col=True, n_cells=0):
    if im_col:
        appx = "_COL"
    else:
        appx = "_B&W"
    # breakpoint()
    X, y = return_resized_cell_array(source_filename, im_col = im_col, n_cells=n_cells)
    type_data = source_filename.split(".")[0]
    filename_path = os.path.join(base_filepath_train_test,f"{type_data}{appx}")
    print(filename_path)
    if n_cells == 0:
        tail = "all"
    else:
        tail = str(n_cells)
    np.save(filename_path+"_X_"+tail,X)
    np.save(filename_path+"_y_"+tail,y)

    print(f"☑️ saved to {filename_path}_X/y_{tail}")

# TESTING
# X, y = return_resized_cell_array(extract_json(load_json("test.json")))
# print(len(X),len(y))

# process_save_array("test.json", im_col = True, n_cells=100)
# process_save_array("test.json", im_col = False, n_cells=1000)
# process_save_array("training.json", im_col = True, n_cells=1000)
# process_save_array("training.json", im_col = False, n_cells=1000)
# process_save_array("test.json", im_col = True)
# process_save_array("test.json", im_col = False)
# process_save_array("training.json", im_col = True)
# process_save_array("training.json", im_col = False)
