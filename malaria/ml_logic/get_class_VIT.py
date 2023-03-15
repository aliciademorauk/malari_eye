import tensorflow as tf
import numpy as np
import pandas as pd
from tensorflow_addons.optimizers import AdamW

export_dir = "vit_classifier"
IMAGE_SIZE = (200,200,3)
def load_VIT_model():

    model = tf.keras.models.load_model(
        export_dir, custom_objects={"AdamW":AdamW}
    )
    return model

def load_test_data(i, j):
    img_array = np.load("../train_test_data/200images/training_COL_X_21778.npy")
    shp = img_array.shape
    print(shp)
    img = img_array[i:j].reshape(-1,*IMAGE_SIZE)
    print(img.shape)
    target_array = np.load("../train_test_data/200images/training_COL_y_21778.npy")
    return img

def predict_on_VIT(model, img):
    pred = model(img)
    output= (tf.math.argmax(pred, axis = 1)) # this picks the highest argument value of the pred return, which
                                             # effectively classifies the image. Shows probabilities
    output_df = pd.DataFrame(output, columns = ["VIT_Type"])

    le_VIT = {0:"gametocyte",
            1:"ring",
            2:"schizont",
            3:"trophozoite"}

    output_df["VIT_Type"].replace(le_VIT, inplace=True)
    infect_results_df = pd.DataFrame(output_df.value_counts())

    return infect_results_df

##FOR TESTING ONLY
# model = load_VIT_model()
# df = predict_on_VIT(model, load_test_data(100,1005))
# print (df)
