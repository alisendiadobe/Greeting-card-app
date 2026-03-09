import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display
import io

# 1. إعداد الصفحة (العنوان الذي يظهر في المتصفح)
st.set_page_config(page_title="بطاقات تهنئة العيد", layout="centered")

# كود لتغيير لون الخلفية وإخفاء القوائم
# يمكنك تغيير #F5F5DC (اللون البيجي) إلى أي كود لون آخر تفضله
custom_style = """
            <style>
            /* تغيير خلفية التطبيق بالكامل */
            .stApp {
                background-color: #F5F5DC; 
            }
            
            /* إخفاء القوائم والعناصر المزعجة */
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden; display: none !important;}
            header {visibility: hidden;}
            div[data-testid="stDecoration"] {display: none !important;}
            .stAppDeployButton {display: none !important;}
            
            /* تحسين شكل خانة إدخال الاسم لتناسب الخلفية الجديدة */
            .stTextInput>div>div>input {
                background-color: #ffffff;
                border-radius: 10px;
            }
            </style>
            """
st.markdown(custom_style, unsafe_allow_html=True)

# 3. القيم الثابتة التي اخترتها أنت (تم تثبيتها لعدم التعديل)
X_CENTER = 2152
Y_POS = 3762
FONT_SIZE = 263
TEXT_COLOR = "#fff204"  # اللون الأصفر الذي اخترته

# 4. مسارات الملفات (تأكد من وجودها في مجلد my_app)
template_path = "my_app/template.jpg"
font_path = "my_app/font.ttf"

st.title("ِEid Greeting Card ✨")
st.write("اكتب اسمك أدناه للحصول على بطاقة التهنئة الخاصة بك")

# خانة إدخال الاسم
name = st.text_input("أدخل الاسم:", "")

if name:
    try:
        # فتح الصورة والخط
        img = Image.open(template_path).convert("RGB")
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(font_path, FONT_SIZE)

        # معالجة اللغة العربية
        reshaped_text = arabic_reshaper.reshape(name)
        bidi_text = get_display(reshaped_text)

        # --- معادلة التوسيط التلقائي ---
        # نحسب عرض النص المدخل مهما كان طوله
        bbox = draw.textbbox((0, 0), bidi_text, font=font)
        text_width = bbox[2] - bbox[0]
        
        # نطرح نصف عرض النص من نقطة المركز (2152) ليبقى دائماً في المنتصف
        adjusted_x = X_CENTER - (text_width / 2)
        # -------------------------------

        # رسم النص على الصورة
        draw.text((adjusted_x, Y_POS), bidi_text, fill=TEXT_COLOR, font=font)

        # عرض المعاينة للمستخدم
        st.image(img, use_column_width=True)

        # زر التحميل
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        st.download_button(
            label="تحميل بطاقتك الآن ✨",
            data=buf.getvalue(),
            file_name=f"Eid_{name}.png",
            mime="image/png"
        )
        
    except Exception as e:
        st.error(f"حدث خطأ: تأكد من رفع الملفات بشكل صحيح. تفاصيل: {e}")

st.divider()
st.caption("كل عام وأنتم بخير")
