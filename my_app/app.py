import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display
import io

# إعداد الصفحة
st.set_page_config(page_title="مصمم بطاقات التهنئة", layout="centered")

st.title("🎨 صانع بطاقات التهنئة الاحترافي")
st.write("اكتب الاسم، اضبط الموقع، ثم حمل بطاقتك")

# المسارات المحدثة لتشمل مجلد my_app
template_path = "my_app/template.png"
font_path = "my_app/font.ttf"

# لوحة التحكم الجانبية
st.sidebar.header("🛠 إعدادات التصميم")
x_pos = st.sidebar.slider("نقطة المنتصف الأفقية (X)", 0, 2000, 1000)
y_pos = st.sidebar.slider("الموقع العمودي (Y)", 0, 2000, 1000)
font_size = st.sidebar.slider("حجم الخط", 10, 300, 80)
text_color = st.sidebar.color_picker("لون الخط", "#000000")

# إدخال الاسم
name = st.text_input("أدخل الاسم الذي تريد طباعته:", "اسم الزميل")

if name:
    try:
        # 1. فتح الصورة
        img = Image.open(template_path).convert("RGB")
        draw = ImageDraw.Draw(img)

        # 2. معالجة النص العربي
        reshaped_text = arabic_reshaper.reshape(name)
        bidi_text = get_display(reshaped_text)

        # 3. تحميل الخط
        font = ImageFont.truetype(font_path, font_size)

        # 4. حساب أبعاد النص لتوسيطه (السر هنا!)
        bbox = draw.textbbox((0, 0), bidi_text, font=font)
        text_width = bbox[2] - bbox[0]
        
        # حساب إحداثي X الجديد ليكون النص دائماً في المنتصف بالنسبة لنقطة X المختارة
        adjusted_x = x_pos - (text_width / 2)

        # 5. الرسم على الصورة
        draw.text((adjusted_x, y_pos), bidi_text, fill=text_color, font=font)

        # عرض المعاينة
        st.image(img, caption="معاينة حية للبطاقة", use_column_width=True)

        # 6. زر التحميل
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        st.download_button(
            label="تحميل البطاقة الآن ✨",
            data=buf.getvalue(),
            file_name=f"greeting_{name}.png",
            mime="image/png"
        )
        
    except FileNotFoundError:
        st.error(f"خطأ: لم يتم العثور على الملفات في مسار {template_path}. تأكد من صحة أسماء الملفات داخل مجلد my_app.")
    except Exception as e:
        st.error(f"حدث خطأ غير متوقع: {e}")
