import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display
import io

st.set_page_config(page_title="مصمم التهنئة الذكي", layout="centered")

st.title("🎨 صانع بطاقات التهنئة العربية")
st.write("اضبط الإعدادات ثم اكتب الاسم لرؤية النتيجة فوراً")

template_path = "my_app/template.png" 

# بدلاً من الـ Sliders، نضع الأرقام التي اخترتها أنت
x_pos = 402  # ضع رقمك هنا
y_pos = 1000 # ضع رقمك هنا
font_size = 55 # ضع رقمك هنا
text_color = "#FFFFFF" # أو اللون الذي اعتمدته

name = st.text_input("Your name:", "Your Name")

if name:
    try:
        img = Image.open(template_path).convert("RGB")
        draw = ImageDraw.Draw(img)
        r        # 1. معالجة النص العربي
        reshaped_text = arabic_reshaper.reshape(name)
        bidi_text = get_display(reshaped_text)
        
        # 2. تحميل الخط
        font = ImageFont.truetype("font.ttf", font_size)

        # 3. حساب حجم النص لتوسيطه تلقائياً
        # نستخدم getbbox للحصول على أبعاد النص (اليسار، الأعلى، اليمين، الأسفل)
        left, top, right, bottom = draw.textbbox((0, 0), bidi_text, font=font)
        text_width = right - left
        
        # 4. حساب الإحداثيات الجديدة ليكون الـ X هو المركز
        # إذا كنت تريد المركز في 500 مثلاً، فسنطرح نصف عرض النص منه
        centered_x = x_pos - (text_width / 2)

        # 5. الكتابة بالمركز الجديد
        draw.text((centered_x, y_pos), bidi_text, fill=text_color, font=font)
        
        # تأكد أن اسم الملف هنا يطابق ملف الخط الذي رفعته (مثلاً font.ttf)
        font = ImageFont.truetype("my_app/font.ttf", font_size)

        draw.text((x_pos, y_pos), bidi_text, fill=text_color, font=font)
        st.image(img, caption="[Preview Card", use_column_width=True)

        buf = io.BytesIO()
        img.save(buf, format="PNG")
        st.download_button(
            label="Download your card ✨",
            data=buf.getvalue(),
            file_name=f"greeting_{name}.png",
            mime="image/png"
        )
    except Exception as e:
        st.error(f"حدث خطأ: تأكد من ملف الصورة والخط. التفاصيل: {e}")
