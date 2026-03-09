import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display
import io
import base64

# 1. إعداد الصفحة
st.set_page_config(page_title="معايدة عيد الفطر", layout="centered")

# وظيفة لتحويل صورة الخلفية المحلية لتظهر في المتصفح
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# 2. تصميم CSS المتكامل (الخلفية، إخفاء العناصر، وتنسيق المربعات)
try:
    bin_str = get_base64('my_app/bg_eid.jpg')
    bg_style = f'background-image: url("data:image/png;base64,{bin_str}");'
except:
    bg_style = 'background-color: #F5F5DC;' # لون احتياطي بيج في حال لم يجد الصورة

custom_style = f"""
    <style>
    /* تطبيق الخلفية وإعدادات الصفحة */
    .stApp {{
        {bg_style}
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    
    /* جعل منطقة المحتوى (المربع الأبيض الشفاف) */
    .main .block-container {{
        background-color: rgba(255, 255, 255, 0.85); 
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-top: 20px;
    }}

    /* إخفاء شعارات Streamlit والقوائم */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden; display: none !important;}}
    header {{visibility: hidden;}}
    div[data-testid="stDecoration"] {{display: none !important;}}
    .stAppDeployButton {{display: none !important;}}

    /* تحسين شكل خانة الإدخال */
    .stTextInput>div>div>input {{
        border: 2px solid #fff204;
        border-radius: 10px;
    }}
    
    /* تنسيق العنوان */
    h1 {{
        color: #4B3621;
        text-align: center;
    }}
    </style>
    """
st.markdown(custom_style, unsafe_allow_html=True)

# 3. الثوابت التي حددتها أنت مسبقاً
X_CENTER = 2152
Y_POS = 3762
FONT_SIZE = 263
TEXT_COLOR = "#fff204"
TEMPLATE_PATH = "my_app/template.jpg"
FONT_PATH = "my_app/font.ttf"

# 4. واجهة التطبيق
st.markdown("<h1>🌙 معايدة عيد الفطر المبارك</h1>", unsafe_allow_html=True)
st.write("<p style='text-align: center; color: #4B3621;'>يسرنا أن نشارككم الفرحة، اكتب اسمك لتجهيز بطاقتك</p>", unsafe_allow_html=True)

name = st.text_input("", placeholder="اكتب اسمك هنا...")

if name:
    try:
        # معالجة الصورة
        img = Image.open(TEMPLATE_PATH).convert("RGB")
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

        reshaped_text = arabic_reshaper.reshape(name)
        bidi_text = get_display(reshaped_text)

        # التوسيط التلقائي
        bbox = draw.textbbox((0, 0), bidi_text, font=font)
        text_width = bbox[2] - bbox[0]
        adjusted_x = X_CENTER - (text_width / 2)

        # رسم النص
        draw.text((adjusted_x, Y_POS), bidi_text, fill=TEXT_COLOR, font=font)

        # عرض النتيجة
        st.image(img, use_column_width=True)

        # زر التحميل بتنسيق أنيق
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        st.download_button(
            label="تحميل البطاقة ✨",
            data=buf.getvalue(),
            file_name=f"Eid_{name}.png",
            mime="image/png"
        )
        
    except Exception as e:
        st.error(f"يرجى التأكد من رفع ملفات الصور والخط بشكل صحيح: {e}")

st.markdown("<br><p style='text-align: center; opacity: 0.5;'>كل عام وأنتم بخير</p>", unsafe_allow_html=True)
