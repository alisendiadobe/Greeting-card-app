import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display
import io

# إعداد الصفحة
st.set_page_config(page_title="Ramadan Greeting Card", layout="centered")
# كود سحري لإخفاء القائمة، العلامة المائية، وأي إشارة للمطور في الأسفل
hide_st_style = """
            <style>
            header {visibility: hidden;}
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden; display: none !important;}
            div[data-testid="stDecoration"] {display: none !important;}
            .stAppDeployButton {display: none !important;}
            section[data-testid="stSidebar"] {display: none !important;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.title("🌙 Ramadan Greeting Card")
st.write("Put your name and download ✨")

# المسارات
template_path = "my_app/template.png"
font_path = "my_app/font.ttf"

# --- القيم الثابتة (استبدل الأرقام أدناه بما ضبطته أنت) ---
X_CENTER = 525  # ضع رقم الـ X هنا
Y_POS = 1000     # ضع رقم الـ Y هنا
FONT_SIZE = 60   # ضع حجم الخط هنا
TEXT_COLOR = "#f4b71c" # ضع كود اللون هنا (مثل #000000 للأسود)
# -------------------------------------------------------

# إدخال الاسم (بدون لوحة جانبية)
name = st.text_input("Name Here:", "")

if name:
    try:
        img = Image.open(template_path).convert("RGB")
        draw = ImageDraw.Draw(img)

        reshaped_text = arabic_reshaper.reshape(name)
        bidi_text = get_display(reshaped_text)

        font = ImageFont.truetype(font_path, FONT_SIZE)

        # الحساب التلقائي للتوسط بناءً على القيمة الثابتة X_CENTER
        bbox = draw.textbbox((0, 0), bidi_text, font=font)
        text_width = bbox[2] - bbox[0]
        adjusted_x = X_CENTER - (text_width / 2)

        draw.text((adjusted_x, Y_POS), bidi_text, fill=TEXT_COLOR, font=font)

        st.image(img, use_column_width=True)

        buf = io.BytesIO()
        img.save(buf, format="PNG")
        st.download_button(
            label="Download Now ✨",
            data=buf.getvalue(),
            file_name=f"greeting_{name}.png",
            mime="image/png"
        )
        
    except Exception as e:
        st.error(f"حدث خطأ: {e}")
