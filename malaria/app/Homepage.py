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

st.set_page_config(page_title='Malari-Eye | AI Diagnostics',
                   page_icon=malari_eye_logo,
                   layout='wide'
)

st.markdown("<h1 style='text-align: right; color: black;'>Microscopy results with the speed of RDTs.</h1>",
            unsafe_allow_html=True)
st.markdown("<h4 style='text-align: right; color: black;'>Convolutional Neural Networks (CNNs) for malaria-paratysized cell identification.</h1>",
            unsafe_allow_html=True)
# st.subheader('Convolutional Neural Networks (CNNs) for malaria-paratysized cell identification.')

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

# malaria metrics -- CSS styling in corresponding file

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}<style>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
original_title = '<p style="font-family:Courier; color:Blue; font-size: 20px;">Original image</p>'
col1.metric("70 °F", "Temperature")
col2.metric("9 mph", "Wind")
col3.metric("86%", "Humidity")

# Malari_Eye intro

# col_title, col_subtitle = st.columns([2, 1])
# col_title.title('Microscopy results with the speed of RDTs.')
# col_subtitle.subheader('Convolutional Neural Networks (CNNs) for malaria-paratysized cell identification.')

col1, col2, col3, col4, = st.columns([1,5,5,1])

col2.image(malaria_parasite, width=350)
col3.image(malaria_parasite_bright, width=415)
