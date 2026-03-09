import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display
import io

# 1. إعداد الصفحة
st.set_page_config(page_title="مصمم بطاقات العيد", layout="centered")

# 2. كود إخفاء العناصر المزعجة (جرب هذا الإصدار الأحدث)
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden; display: none !important;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 3. وضع المطور (خيار سري للتعديل)
dev_mode = st.sidebar.checkbox("🛠 وضع الضبط (تعديل التصميم)")

# القيم الافتراضية (عدلها هنا مرة واحدة)
X_VAL, Y_VAL, SIZE_VAL = 1000, 1200, 90
COLOR_VAL = "#000000"

if dev_mode:
    st.sidebar.info("ضبط إحداثيات العيد الجديد:")
    X_VAL = st.sidebar.slider("نقطة المنتصف X", 0, 3000, 1000)
    Y_VAL = st.sidebar.slider("الموقع العمودي Y", 0, 3000, 1200)
    SIZE_VAL = st.sidebar.slider("حجم الخط", 10, 500, 90)
    COLOR_VAL = st.sidebar.color_picker("لون الخط", "#000000")
    # طباعة القيم الحالية ليسهل عليك نسخها لاحقاً
    st.sidebar.code(f"X: {X_VAL}, Y: {Y_VAL}\nSize: {SIZE_VAL}")

# 4. المسارات (تأكد من رفع صورة العيد الجديدة باسم eid_template.jpg)
template_path = "my_app/eid_template.jpg" 
font_path = "my_app/font.ttf"

st.title("🌙 تهنئة عيد الفطر المبارك")
name = st.text_input("أدخل الاسم الذي تريد وضعه على بطاقة العيد:", "")

if name:
    try:
        img = Image.open(template_path).convert("RGB")
        draw = ImageDraw.Draw(img)
        reshaped_text = arabic_reshaper.reshape(name)
        bidi_text = get_display(reshaped_text)
        font = ImageFont.truetype(font_path, SIZE_VAL)

        # التوسيط التلقائي السحري
        bbox = draw.textbbox((0, 0), bidi_text, font=font)
        text_width = bbox[2] - bbox[0]
        adjusted_x = X_VAL - (text_width / 2)

        draw.text((adjusted_x, Y_VAL), bidi_text, fill=COLOR_VAL, font=font)
        st.image(img, use_column_width=True)

        # زر التحميل
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        st.download_button(label="تحميل بطاقة العيد ✨", data=buf.getvalue(), file_name=f"Eid_{name}.png")
        
    except Exception as e:
        st.error(f"تأكد من رفع الصورة الجديدة: {e}")
