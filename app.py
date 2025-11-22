import streamlit as st
import pandas as pd
from pathlib import Path

# ---------- إعداد الصفحة ----------
st.set_page_config(
    page_title="Student Grades",
    page_icon="📚",
    layout="centered"
)

# ---------- تحميل الخط + تنسيق CSS ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Tajawal', sans-serif;
}

/* card style */
.block-container {
    padding-top: 40px !important;
}

/* center logo */
.logo-container {
    display: flex;
    justify-content: center;
    margin-bottom: 20px;
}

/* search box in center */
.search-area {
    display: flex;
    justify-content: center;
}

/* make table smaller + RTL */
.small-table table {
    direction: rtl;
    font-size: 16px;
}

.small-table th {
    background: #007bff !important;
    color: white !important;
    text-align: center !important;
}

.small-table td {
    text-align: center !important;
}
</style>
""", unsafe_allow_html=True)

# ---------- المسار ----------
DATA_PATH = Path("grades.xlsx")

@st.cache_data(ttl=60)
def load_data(path):
    try:
        df = pd.read_excel(path, engine="openpyxl")
        return df
    except Exception as e:
        st.error(f"خطأ في قراءة الملف: {e}")
        return None

# ---------- واجهة البرنامج ----------
# اللوجو في المنتصف
st.markdown('<div class="logo-container">', unsafe_allow_html=True)
st.image("logo.png", width=200)   # ← غيّر اسم الصورة حسب ملفك
st.markdown('</div>', unsafe_allow_html=True)

# العنوان
st.markdown("<h2 style='text-align:center; color:#333;'>📚 نظام عرض درجات الطلاب</h2>", unsafe_allow_html=True)

df = load_data(DATA_PATH)

if df is not None:

    st.write("")  # مسافة بسيطة

    # البحث في المنتصف
    st.markdown('<div class="search-area">', unsafe_allow_html=True)
    search_by = st.radio("البحث بواسطة:", ["ID", "الاسم"], horizontal=True)
    st.markdown('</div>', unsafe_allow_html=True)

    query = st.text_input("اكتب ID أو الاسم هنا:")

    if query:
        if search_by == "ID":
            try:
                qnum = float(query)
                results = df[df.iloc[:, 0] == qnum]
            except:
                results = df[df.iloc[:, 0].astype(str).str.contains(query, na=False)]
        else:
            results = df[df.iloc[:, 1].astype(str).str.contains(query, case=False, na=False)]

        if not results.empty:
            st.success(f"تم العثور على {len(results)} نتيجة")

            st.markdown('<div class="small-table">', unsafe_allow_html=True)
            st.dataframe(results, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        else:
            st.info("لا توجد نتائج للبحث.")

else:
    st.warning("⚠️ ملف البيانات غير موجود.")
