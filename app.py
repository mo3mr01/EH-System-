import streamlit as st
import pandas as pd
from pathlib import Path

# ---------------------------
# إعداد الصفحة + اللوجو
# ---------------------------
st.set_page_config(page_title="Student Grades Viewer", layout="wide")

# ضع اللوجو في نفس مجلد الملف باسم logo.png
try:
    st.image("logo.png", width=200)
except:
    pass

st.title("🎓 Student Grades Viewer")

# ---------------------------
# تحميل البيانات + تجهيز الأعمدة
# ---------------------------
DATA_PATH = Path("grades.xlsx")

@st.cache_data(ttl=60)
def load_grades():
    if not DATA_PATH.exists():
        return None
    try:
        df = pd.read_excel(DATA_PATH)

        # الأعمدة الأساسية المطلوبة
        required_cols = ["الاســــــــــــم", "رقم الطالب", "رقم ولي الأمر"]

        # تأكد أن الأعمدة موجودة
        for col in required_cols:
            if col not in df.columns:
                st.error(f"❌ العمود '{col}' غير موجود داخل ملف Excel!")
                return None

        # ترتيب الأعمدة: الأساسية ثم باقي الأعمدة
        other_cols = [c for c in df.columns if c not in required_cols]
        df = df[required_cols + other_cols]

        return df

    except Exception as e:
        st.error(f"خطأ أثناء قراءة الملف: {e}")
        return None


df = load_grades()

# ---------------------------
# واجهة البحث
# ---------------------------
if df is None:
    st.warning("⚠️ ملف الدرجات غير موجود أو به مشكلة. تأكد من وجود grades.xlsx في نفس المجلد.")
else:
    search_by = st.radio("البحث بواسطة:", ["اسم الطالب", "رقم الطالب", "رقم ولي الأمر"])
    query = st.text_input("اكتب ما تبحث عنه هنا:")

    filtered = df.copy()

    if query:
        if search_by == "اسم الطالب":
            filtered = df[df["الاســــــــــــم"].astype(str).str.contains(query, case=False, na=False)]

        elif search_by == "رقم الطالب":
            filtered = df[df["رقم الطالب"].astype(str).str.contains(query, na=False)]

        elif search_by == "رقم ولي الأمر":
            filtered = df[df["رقم ولي الأمر"].astype(str).str.contains(query, na=False)]

    # ---------------------------
    # عرض النتائج
    # ---------------------------
    if not filtered.empty:
        st.success(f"تم العثور على {len(filtered)} نتيجة")
        st.dataframe(filtered, use_container_width=True)

        # زر التحميل
        csv = filtered.to_csv(index=False)
        st.download_button(
            "تحميل النتائج (CSV)",
            data=csv,
            file_name="filtered_results.csv",
            mime="text/csv"
        )
    else:
        if query:
            st.info("لا توجد نتائج مطابقة لبحثك.")



