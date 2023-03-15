import torch
from IPython.core.debugger import set_trace
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.patches import Rectangle
import numpy as np
from PIL import Image
import cv2

torch.hub._validate_not_a_forked_repo=lambda a,b,c: True

def import_pytorch_model(arr_img):
    # fetching model
    model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt', force_reload=True)
    # Image
     # Inference
    results = model(arr_img)
    # Results, change the flowing to: results.show()
    # results.show()  # or .show(), .save(), .crop(), .pandas(), etc
    results.xyxy[0]  # im predictions (tensor)
    df = results.pandas().xyxy[0]  # im predictions (pandas)
    # breakpoint()
    return df

def get_bounding_box_image(df, image_path):
    # Load the image
    # Define the boxes
    boxes = []
    for index, row in df.iterrows():
        x = round(row['xmin'])
        y = round(row['ymin'])
        x_max = round(row['xmax'])
        y_max = round(row['ymax'])
        # breakpoint()
        image_path = cv2.rectangle(image_path, (x, y), (x_max, y_max), (255,0,0), 2)
    # Add the boxes to the plot

    # Image.fromarray(image_path).show()
    return image_path


def get_bounding_box_count(df):
    return len(df)

img = Image.open("./0a7bfa8a-ee52-4f7a-b9c5-2919ecfa93ef.png")
img.show()
# breakpoint()
df = import_pytorch_model(np.asarray(img))
get_bounding_box_image(df, np.asarray(img))
# df.to_csv("arnaud_yolo")
print (get_bounding_box_count)
