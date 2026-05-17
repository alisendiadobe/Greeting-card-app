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

# 2. Design & CSS
bg_image_path = 'my_app/bg_eid.jpg'
bin_str = get_base64_bin(bg_image_path)

if bin_str:
    bg_style = f'background-image: url("data:image/jpeg;base64,{bin_str}");'
else:
    bg_style = 'background-color: #f7ece4;'

custom_style = f"""
    <style>
    .stApp {{
        {bg_style}
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    .main .block-container {{
        background-color: rgba(255, 255, 255, 0.85); 
        padding: 40px;
        border-radius: 1px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-top: 20px;
    }}
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden; display: none !important;}}
    header {{visibility: hidden;}}
    /* Golden Button Style */
    .stDownloadButton > button {{
        background-color: #ccb8aa !important;
        color: #4B3621 !important;
        border: none;
        border-radius: 12px;
        font-weight: bold;
        width: 100%;
        height: 50px;
        font-size: 18px;
    }}
    h1, p {{
        color: #4f3828 !important;
        text-align: center;
    }}
    </style>
    """
st.markdown(custom_style, unsafe_allow_html=True)

# 3. Fixed Coordinates and Values (Your specific settings)
X_CENTER = 2152
Y_POS = 3600
FONT_SIZE = 180
TEXT_COLOR = "#006937"
TEMPLATE_PATH = "my_app/template.jpg"
FONT_PATH = "my_app/font.ttf"

# 4. App Interface
st.markdown("<h1>✨ Eid Greeting Card✨ </h1>", unsafe_allow_html=True)
st.markdown("<p>Share the happiness! Enter your name below to generate your card.</p>", unsafe_allow_html=True)

name = st.text_input("", placeholder="Type your name here...")

if name:
    try:
        img = Image.open(TEMPLATE_PATH).convert("RGB")
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

        reshaped_text = arabic_reshaper.reshape(name)
        bidi_text = get_display(reshaped_text)

        # Correcting the line that caused the error
        bbox = draw.textbbox((0, 0), bidi_text, font=font)
        text_width = bbox[2] - bbox[0]
        adjusted_x = X_CENTER - (text_width / 2)

        draw.text((adjusted_x, Y_POS), bidi_text, fill=TEXT_COLOR, font=font)

        st.image(img, use_column_width=True)

        buf = io.BytesIO()
        img.save(buf, format="PNG")
        st.download_button(
            label="Download Your Card ✨",
            data=buf.getvalue(),
            file_name=f"Eid_Card_{name}.png",
            mime="image/png"
        )
  
    except Exception as e:
        st.error(f"Error loading files. Check if 'template.jpg' exists in 'my_app' folder.")

st.markdown("<br><p style='opacity: 0.6;'>Happy Eid to you and your family!</p>", unsafe_allow_html=True)
