{\rtf1\ansi\ansicpg1252\cocoartf2759
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import streamlit as st\
from PIL import Image, ImageDraw, ImageFont\
import arabic_reshaper\
from bidi.algorithm import get_display\
import io\
\
st.set_page_config(page_title="\uc0\u1605 \u1589 \u1605 \u1605  \u1575 \u1604 \u1578 \u1607 \u1606 \u1574 \u1577  \u1575 \u1604 \u1584 \u1603 \u1610 ", layout="centered")\
\
st.title("\uc0\u55356 \u57256  \u1589 \u1575 \u1606 \u1593  \u1576 \u1591 \u1575 \u1602 \u1575 \u1578  \u1575 \u1604 \u1578 \u1607 \u1606 \u1574 \u1577  \u1575 \u1604 \u1593 \u1585 \u1576 \u1610 \u1577 ")\
st.write("\uc0\u1575 \u1590 \u1576 \u1591  \u1575 \u1604 \u1573 \u1593 \u1583 \u1575 \u1583 \u1575 \u1578  \u1579 \u1605  \u1575 \u1603 \u1578 \u1576  \u1575 \u1604 \u1575 \u1587 \u1605  \u1604 \u1585 \u1572 \u1610 \u1577  \u1575 \u1604 \u1606 \u1578 \u1610 \u1580 \u1577  \u1601 \u1608 \u1585 \u1575 \u1611 ")\
\
# \uc0\u1585 \u1601 \u1593  \u1605 \u1604 \u1601  \u1575 \u1604 \u1578 \u1605 \u1576 \u1604 \u1578 \
template_path = "template.jpg" # \uc0\u1578 \u1571 \u1603 \u1583  \u1605 \u1606  \u1608 \u1580 \u1608 \u1583  \u1575 \u1604 \u1589 \u1608 \u1585 \u1577  \u1576 \u1606 \u1601 \u1587  \u1575 \u1604 \u1605 \u1580 \u1604 \u1583 \
\
# \uc0\u1573 \u1593 \u1583 \u1575 \u1583 \u1575 \u1578  \u1575 \u1604 \u1578 \u1581 \u1603 \u1605  (Sliders) \u1604 \u1578 \u1587 \u1607 \u1610 \u1604  \u1575 \u1604 \u1578 \u1606 \u1587 \u1610 \u1602 \
st.sidebar.header("\uc0\u1573 \u1593 \u1583 \u1575 \u1583 \u1575 \u1578  \u1575 \u1604 \u1606 \u1589 ")\
x_pos = st.sidebar.slider("\uc0\u1575 \u1604 \u1605 \u1608 \u1602 \u1593  \u1575 \u1604 \u1571 \u1601 \u1602 \u1610  (X)", 0, 2000, 500)\
y_pos = st.sidebar.slider("\uc0\u1575 \u1604 \u1605 \u1608 \u1602 \u1593  \u1575 \u1604 \u1593 \u1605 \u1608 \u1583 \u1610  (Y)", 0, 2000, 500)\
font_size = st.sidebar.slider("\uc0\u1581 \u1580 \u1605  \u1575 \u1604 \u1582 \u1591 ", 20, 200, 70)\
text_color = st.sidebar.color_picker("\uc0\u1604 \u1608 \u1606  \u1575 \u1604 \u1582 \u1591 ", "#000000")\
\
name = st.text_input("\uc0\u1571 \u1583 \u1582 \u1604  \u1575 \u1604 \u1575 \u1587 \u1605  \u1607 \u1606 \u1575 :", "\u1575 \u1587 \u1605  \u1575 \u1604 \u1586 \u1605 \u1610 \u1604 ")\
\
if name:\
    try:\
        img = Image.open(template_path).convert("RGB")\
        draw = ImageDraw.Draw(img)\
\
        # 1. \uc0\u1605 \u1593 \u1575 \u1604 \u1580 \u1577  \u1575 \u1604 \u1606 \u1589  \u1575 \u1604 \u1593 \u1585 \u1576 \u1610  (\u1575 \u1604 \u1585 \u1576 \u1591  \u1608 \u1575 \u1604 \u1575 \u1578 \u1580 \u1575 \u1607 )\
        reshaped_text = arabic_reshaper.reshape(name)\
        bidi_text = get_display(reshaped_text)\
\
        # 2. \uc0\u1578 \u1581 \u1605 \u1610 \u1604  \u1575 \u1604 \u1582 \u1591  (\u1578 \u1571 \u1603 \u1583  \u1605 \u1606  \u1608 \u1580 \u1608 \u1583  \u1605 \u1604 \u1601  \u1582 \u1591  \u1593 \u1585 \u1576 \u1610  .ttf)\
        # \uc0\u1605 \u1579 \u1575 \u1604 : 'Amiri-Regular.ttf' \u1571 \u1608  'Arial.ttf'\
        font = ImageFont.truetype("Arial.ttf", font_size)\
\
        # 3. \uc0\u1575 \u1604 \u1603 \u1578 \u1575 \u1576 \u1577  \u1593 \u1604 \u1609  \u1575 \u1604 \u1589 \u1608 \u1585 \u1577 \
        draw.text((x_pos, y_pos), bidi_text, fill=text_color, font=font)\
\
        # \uc0\u1593 \u1585 \u1590  \u1575 \u1604 \u1605 \u1593 \u1575 \u1610 \u1606 \u1577 \
        st.image(img, caption="\uc0\u1605 \u1593 \u1575 \u1610 \u1606 \u1577  \u1575 \u1604 \u1576 \u1591 \u1575 \u1602 \u1577 ", use_column_width=True)\
\
        # 4. \uc0\u1586 \u1585  \u1575 \u1604 \u1578 \u1581 \u1605 \u1610 \u1604 \
        buf = io.BytesIO()\
        img.save(buf, format="PNG")\
        st.download_button(\
            label="\uc0\u1578 \u1581 \u1605 \u1610 \u1604  \u1575 \u1604 \u1576 \u1591 \u1575 \u1602 \u1577  \u1575 \u1604 \u1570 \u1606  \u10024 ",\
            data=buf.getvalue(),\
            file_name=f"greeting_\{name\}.png",\
            mime="image/png"\
        )\
    except Exception as e:\
        st.error(f"\uc0\u1581 \u1583 \u1579  \u1582 \u1591 \u1571 : \u1578 \u1571 \u1603 \u1583  \u1605 \u1606  \u1608 \u1580 \u1608 \u1583  \u1605 \u1604 \u1601  \u1575 \u1604 \u1589 \u1608 \u1585 \u1577  \u1608 \u1575 \u1604 \u1582 \u1591 . \u1575 \u1604 \u1578 \u1601 \u1575 \u1589 \u1610 \u1604 : \{e\}")\
}