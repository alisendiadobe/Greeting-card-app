import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display
import io
import base64
import os

# 1. Page Configuration
st.set_page_config(page_title="Eid Greeting Card", layout="centered")

# Function to safely load the background image
def get_base64_bin(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

# 2. Design & CSS (English UI + Color Updates)
# We will use the Beige color as a fallback if the image fails
bg_image_path = 'my_app/bg_eid.jpg'
bin_str = get_base64_bin(bg_image_path)

if bin_str:
    bg_style = f'background-image: url("data:image/jpeg;base64,{bin_str}");'
else:
    bg_style = 'background-color: #F5F5DC;' # Fallback to Beige

custom_style = f"""
    <style>
    .stApp {{
        {bg_style}
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    
    /* Content box transparency */
    .main .block-container {{
        background-color: rgba(255, 255, 255, 0.85); 
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-top: 20px;
    }}

    /* Hide Streamlit elements */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden; display: none !important;}}
    header {{visibility: hidden;}}
    div[data-testid="stDecoration"] {{display: none !important;}}
    .stAppDeployButton {{display: none !important;}}

    /* Input field styling - Golden border */
    .stTextInput>div>div>input {{
        border: 2px solid #fff204;
        border-radius: 10px;
    }}
    
    /* Heading Color (Brown/Coffee for better contrast on Beige) */
    h1 {{
        color: #4B3621 !important;
        text-align: center;
    }}
    p {{
        color: #4B3621 !important;
        text-align: center;
    }}
    </style>
    """
st.markdown(custom_style, unsafe_allow_html=True)

# 3. Fixed Coordinates and Values
X_CENTER = 2152
Y_POS = 3762
FONT_SIZE = 263
TEXT_COLOR = "#fff204" # Your chosen yellow for the name
TEMPLATE_PATH = "my_app/template.jpg"
FONT_PATH = "my_app/font.ttf"

# 4. App Interface (English)
st.markdown("<h1>✨ Eid Greeting Card</h1>", unsafe_allow_html=True)
st.markdown("<p>Share the happiness! Enter your name below to generate your card.</p>", unsafe_allow_html=True)

name = st.text_input("", placeholder="Type your name here...")

if name:
    try:
        # Image Processing
        img = Image.open(TEMPLATE_PATH).convert("RGB")
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

        # Arabic/Bidi Support
        reshaped_text = arabic_reshaper.reshape(name)
        bidi_text = get_display(reshaped_text)

        # Auto-Centering Logic
        bbox = draw.
