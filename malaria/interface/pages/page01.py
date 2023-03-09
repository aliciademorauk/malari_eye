import streamlit as st
import numpy as np
from PIL import Image


# Malari_Eye page configuration... background image not working
# our CSS color - #cc2c50

st.set_page_config(layout="wide")
page_background_image = '''
<style>
[data-testid='stAppViewContainer']{
    background-image: url('/Users/aliciademora/Documents/Cells-Background.webp');
}

[data-testid='stHeader']{
    background-color: #cc2c50;
}
</style>
'''

st.markdown(page_background_image, unsafe_allow_html=True)

# Malari_Eye logo and tool intro

col1, col2, col3, col4 = st.columns([1, 4, 3, 1])
malari_eye_logo = Image.open('/Users/aliciademora/Documents/Malaria-Logo.png')
malaria_parasite = Image.open('/Users/aliciademora/Documents/Malaria-Parasite.jpeg')

# Need to update file path to work on all machines.

col2.image(malaria_parasite, width=450)

col3.image(malari_eye_logo, width=250)
col3.subheader('Microscopy results with the speed of RDTs.')
col3.write('Convolutional Neural Networks (CNNs) for malaria-paratysized cell identification.')

# File uploader... need to check what the required output is to pass over to the function

uploaded_file = st.file_uploader('Please upload your blood sample below:', type=None) # Need to specify the file format allowed.
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    st.write(bytes_data)
