import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display
import io

# إعداد الصفحة
st.set_page_config(page_title="مصمم بطاقات التهنئة", layout="centered")

st.title("🎨 صانع بطاقات التهنئة الاحترافي")
st.write("اكتب الاسم، اضبط الموقع، ثم حمل بطاقتك")

# مسار الملفات - تأكد أنها بنفس المجلد على GitHub
# إذا كانت داخل مجلد اسمه my_app، غير المسار إلى "my_app/template.jpg"
template_path = "template.jpg"
font_path = "font.ttf"

# لوحة التحكم الجانبية لضبط الإعدادات بدقة
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

        # 2. معالجة النص العربي (الربط والاتجاه)
        reshaped_text = arabic_reshaper.reshape(name)
        bidi_text = get_display(reshaped_text)

        # 3. تحميل الخط
        font = ImageFont.truetype(font_path, font_size)

        # 4. حساب أبعاد النص لتوسيطه (السر هنا!)
        # نستخدم textbbox لمعرفة عرض النص بدقة
        bbox = draw.textbbox((0, 0), bidi_text, font=font)
        text_width = bbox[2] - bbox[0]
        
        # حساب إحداثي X الجديد (نطرح نصف عرض النص من نقطة المنتصف المختارة)
        # هذا يجعل النص يتمدد لليمين واليسار بالتساوي من المركز
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
        st.error("خطأ: لم يتم العثور على ملف الصورة أو الخط. تأكد من وجود template.jpg و font.ttf")
    except Exception as e:
        st.error(f"حدث خطأ غير متوقع: {e}")

st.divider()
st.info("نصيحة: بعد ضبط الأرقام المثالية، يمكنك تثبيتها في الكود وإخفاء شريط الإعدادات.")
