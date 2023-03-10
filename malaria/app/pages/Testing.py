import streamlit as st
import numpy as np
from PIL import Image
import pandas as pd
import numpy as np

# images

malari_eye_logo = Image.open('/Users/aliciademora/code/aliciademorauk/project/malari_eye/malaria/app/images/Malaria-Logo.png')

# page configuration...

# 1. page title, layout

st.set_page_config(page_title='Malari-Eye | Testing Area',
                   page_icon=malari_eye_logo,
                   layout='wide'
)

# 2. add logo function for sidebar

def add_logo():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: ('/Users/aliciademora/code/aliciademorauk/project/malari_eye/malaria/app/images/Malaria-Logo.png');
                background-repeat: no-repeat;
                padding-top: 120px;
                background-position: 20px 20px;
            }
            [data-testid="stSidebarNav"]::before {
                content: "Menu";
                margin-left: 20px;
                margin-top: 20px;
                margin-bottom: 70px;
                font-size: 30px;
                position: relative;
                top: 100px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

add_logo()

# file uploader... need to check what the required output is to pass over to the function

## file uploader title

st.title('Testing Area')
st.subheader('Please follow the steps below to receive a diagnosis:')

## STEP 1 - upload file

st.header('Step 1')
st.write('Upload a file with the patient\'s blood sample for scanning.')

uploaded_file = st.file_uploader(label='File formats allowed are JPG, JPEG and PNG.') # Need to specify the file format allowed.
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    st.write(bytes_data)

## STEP 2 - loading

st.header('Step 2')
st.write('Our model is able to determine the stage of infection of a malaria-parasitized cell. Your results will be displayed below.')

#### here we need to get the input from the model

results_df = pd.DataFrame(columns=(['Gametocyte', 'Leukocyte', 'Red Blood Cell', 'Ring', 'Schizont','Trophozoite']))

st.table(results_df)
