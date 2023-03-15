import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.patches import Rectangle

# Load the image
image = mpimg.imread('image.jpg')

# load dataframe

df = 'link from get_yolo'

# Plot the image
plt.imshow(image)

# Define the boxes
boxes = []
for index, row in df.iterrows():
    x = row['x']
    y = row['y']
    width = row['width']
    height = row['height']
    boxes.append(Rectangle((x, y), width, height, linewidth=1, edgecolor='r', facecolor='none'))

# Add the boxes to the plot
ax = plt.gca()
for box in boxes:
    ax.add_patch(box)

# Show the image and boxes
plt.show()
