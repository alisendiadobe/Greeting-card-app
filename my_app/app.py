import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display
import io

st.set_page_config(page_title="مصمم التهنئة الذكي", layout="centered")

st.title("🎨 صانع بطاقات التهنئة العربية")
st.write("اضبط الإعدادات ثم اكتب الاسم لرؤية النتيجة فوراً")

template_path = "my_app/template.png" 

st.sidebar.header("إعدادات النص")
x_pos = st.sidebar.slider("الموقع الأفقي (X)", 0, 2000, 500)
y_pos = st.sidebar.slider("الموقع العمودي (Y)", 0, 2000, 500)
font_size = st.sidebar.slider("حجم الخط", 20, 200, 70)
text_color = st.sidebar.color_picker("لون الخط", "#000000")

name = st.text_input("أدخل الاسم هنا:", "اسم الزميل")

if name:
    try:
        img = Image.open(template_path).convert("RGB")
        draw = ImageDraw.Draw(img)
        reshaped_text = arabic_reshaper.reshape(name)
        bidi_text = get_display(reshaped_text)
        
        # تأكد أن اسم الملف هنا يطابق ملف الخط الذي رفعته (مثلاً font.ttf)
        font = ImageFont.truetype("my_app/font.ttf", font_size)

        draw.text((x_pos, y_pos), bidi_text, fill=text_color, font=font)
        st.image(img, caption="معاينة البطاقة", use_column_width=True)

        buf = io.BytesIO()
        img.save(buf, format="PNG")
        st.download_button(
            label="تحميل البطاقة الآن ✨",
            data=buf.getvalue(),
            file_name=f"greeting_{name}.png",
            mime="image/png"
        )
    except Exception as e:
        st.error(f"حدث خطأ: تأكد من ملف الصورة والخط. التفاصيل: {e}")
