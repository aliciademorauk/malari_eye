import streamlit as st
import numpy as np
from PIL import Image
import pandas as pd
import numpy as np

# images:
# need to add images to this folder and update file path.

malaria_parasite_bright = Image.open('/Users/aliciademora/code/aliciademorauk/project/malari_eye/malaria/app/images/Cells-Background.jpeg')
malari_eye_logo = Image.open('/Users/aliciademora/code/aliciademorauk/project/malari_eye/malaria/app/images/Malaria-Logo.png')
malaria_parasite = Image.open('/Users/aliciademora/code/aliciademorauk/project/malari_eye/malaria/app/images/Malaria-Parasite.jpeg')

# page configuration...

# 1. page title, layout

st.set_page_config(page_title='Malari-Eye | The Project',
                   page_icon=malari_eye_logo,
                   layout='wide'
)

# 2. add logo function for sidebar

def add_logo():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: ('/Users/aliciademora/code/aliciademorauk/project/malari_eye/malaria/app/images/Malaria-Logo.png')';
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

# 2. start of page

st.title('About the Project')
st.subheader('How it Works')
st.subheader('Project Inspiration')
st.subheader('Meet the Team')
