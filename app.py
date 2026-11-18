import streamlit as st
from PIL import Image
from PIL.ExifTags import TAGS
import io

# إعدادات الصفحة الأساسية
st.set_page_config(
    page_title="EXIF Forensics & Privacy Shield",
    page_icon="🛡️",
    layout="wide"
)

# حقن كود CSS مخصص لتغيير التصميم بالكامل
st.markdown("""
<style>
    /* تغيير خلفية التطبيق بالكامل */
    .stApp {
        background: linear-gradient(135deg, #090d16 0%, #131b2e 50%, #0d1322 100%);
        color: #e2e8f0;
    }
    
    /* تخصيص العناوين */
    h1, h2, h3 {
        color: #10b981 !important;
        font-family: 'Courier New', monospace;
    }
    
    /* تصميم البطاقات */
    .cyber-card {
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid #10b981;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 20px rgba(16, 185, 129, 0.15);
        margin-bottom: 20px;
    }
    
    /* تخصيص الأزرار */
    .stButton > button {
        background: linear-gradient(90deg, #059669 0%, #10b981 100%);
        color: #ffffff;
        border: none;
        border-radius: 8px;
        font-weight: bold;
        padding: 10px 24px;
        width: 100%;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        box-shadow: 0 0 15px rgba(16, 185, 129, 0.6);
        transform: translateY(-2px);
    }
    
    /* تخصيص القائمة الجانبية */
    [data-testid="stSidebar"] {
        background-color: #0b0f19;
        border-right: 1px solid #1e293b;
    }
</style>
""", unsafe_allow_html=True)

# الشريط الجانبي التعريفي
with st.sidebar:
    st.markdown("## 🛡️ مركز التحليل الرقمي")
    st.markdown("---")
    st.info("**الوظيفة:** استخراج البيانات الوصفية (EXIF) وتطهير الصور لحماية الخصوصية من تتبع الـ OSINT.")
    st.markdown("### ⚙️ الوضع المختار:")
    mode = st.radio(
        "اختر العملية المطلوبة:",
        ["🔍 وضع الفحص والاستخراج (Inspector)", "🧹 وضع التطهير والحماية (Cleaner)"]
    )
    st.markdown("---")
    st.caption("تطوير: شهد عامر | قسم هندسة تقنيات الأمن السيبراني")

# وظيفة استخراج بيانات EXIF
def get_exif_data(image):
    exif_info = {}
    try:
        exifdata = image._getexif()
        if exifdata:
            for tag_id, value in exifdata.items():
                tag = TAGS.get(tag_id, tag_id)
                if isinstance(value, bytes):
                    try:
                        value = value.decode('utf-8', errors='ignore')
                    except:
                        value = str(value)
                exif_info[str(tag)] = str(value)
    except Exception:
        pass
    return exif_info

# وظيفة حذف بيانات EXIF
def remove_exif_data(image):
    data = list(image.getdata())
    clean_img = Image.new(image.mode, image.size)
    clean_img.putdata(data)
    return clean_img

# ترويسة الصفحة الرئيسية
st.markdown("<h1 style='text-align: center;'>[ EXIF METADATA FORENSICS LAB ]</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8;'>مختبر تحليل البصمة الرقمية للصور وحماية الخصوصية</p>", unsafe_allow_html=True)
st.write("---")

if mode == "🔍 وضع الفحص والاستخراج (Inspector)":
    st.markdown('<div class="cyber-card">', unsafe_allow_html=True)
    st.subheader("📡 رفع الهدف لفحص البيانات الخفية")
    uploaded_file = st.file_uploader("اسحب الصورة هنا أو اخترها من جهازك (JPG/PNG):", type=["jpg", "jpeg", "png"], key="inspect_file")
    st.markdown('</div>', unsafe_allow_html=True)

    if uploaded_file:
        image = Image.open(uploaded_file)
        col1, col2 = st.columns([1, 1.5])
        
        with col1:
            st.markdown('<div class="cyber-card">', unsafe_allow_html=True)
            st.image(image, caption="معاينة الصورة الهدف", use_container_width=True)
            st.write(f"**الأبعاد:** {image.size[0]} x {image.size[1]} بكسل")
            st.write(f"**الصيغة:** {image.format}")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col2:
            st.markdown('<div class="cyber-card">', unsafe_allow_html=True)
            st.subheader("📑 نتائج التحليل الجنائي للبيانات")
            if st.button("🚀 بدء الفحص العميق (Scan Metadata)"):
                with st.spinner("جاري تحليل ترويسات الصورة..."):
                    exif_data = get_exif_data(image)
                    if exif_data:
                        st.success(f"⚠️ تم رصد {len(exif_data)} سجل بيانات وصفية داخل الصورة!")
                        st.json(exif_data)
                    else:
                        st.warning("✅ الصورة نظيفة ولا تحتوي على أي بيانات وصفية (EXIF) قابلة للاستخراج.")
            st.markdown('</div>', unsafe_allow_html=True)

elif mode == "🧹 وضع التطهير والحماية (Cleaner)":
    st.markdown('<div class="cyber-card">', unsafe_allow_html=True)
    st.subheader("🛡️ تطهير الصورة وإزالة آثار التتبع الجغرافي والتقني")
    clean_file = st.file_uploader("اختر الصورة المراد تأمينها قبل النشر:", type=["jpg", "jpeg", "png"], key="clean_file")
    st.markdown('</div>', unsafe_allow_html=True)

    if clean_file:
        img_to_clean = Image.open(clean_file)
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="cyber-card">', unsafe_allow_html=True)
            st.image(img_to_clean, caption="الصورة الأصلية (قد تحتوي على بيانات تتبع)", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col2:
            st.markdown('<div class="cyber-card">', unsafe_allow_html=True)
            st.subheader("⚙️ المعالجة والحفظ الآمن")
            st.write("سيتم إنشاء نسخة جديدة كلياً من البكسلات فقط دون أي ترويسات مخفية.")
            if st.button("⚡ تنفيذ التطهير الآن (Wipe EXIF)"):
                cleaned_image = remove_exif_data(img_to_clean)
                buf = io.BytesIO()
                img_format = img_to_clean.format if img_to_clean.format in ["JPEG", "PNG"] else "JPEG"
                cleaned_image.save(buf, format=img_format)
                
                st.success("🔒 تم مسح كافة البيانات بنجاح!")
                st.download_button(
                    label="📥 تحميل النسخة المؤمّنة والنظيفة",
                    data=buf.getvalue(),
                    file_name="secured_clean_image.jpg",
                    mime=f"image/{img_format.lower()}"
                )
            st.markdown('</div>', unsafe_allow_html=True)
