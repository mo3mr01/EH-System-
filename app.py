# app.py
import streamlit as st
import pandas as pd
from backend import load_grades

st.set_page_config(page_title="Student Grades Viewer", layout="wide")

# --- عرض اللوجو ---
st.image("logo.png", width=200)

st.title("🎓 Student Grades Viewer")

df = load_grades()

if df is None:
    st.warning("⚠️ ملف الدرجات غير موجود أو به مشكلة.")
else:
    # اختيار البحث
    search_by = st.radio("البحث بواسطة:", ["اسم الطالب", "رقم الطالب", "رقم ولي الأمر"])

    query = st.text_input("اكتب ما تبحث عنه هنا:")

    filtered = df.copy()

    if query:
        if search_by == "اسم الطالب":
            filtered = df[df["الاسم"].astype(str).str.contains(query, case=False, na=False)]

        elif search_by == "رقم الطالب":
            filtered = df[df["رقم_الطالب"].astype(str).str.contains(query, na=False)]

        else:
            filtered = df[df["رقم_ولي_الامر"].astype(str).str.contains(query, na=False)]

    # إذا في نتائج
    if not filtered.empty:
        st.success(f"تم العثور على {len(filtered)} نتيجة")
        st.dataframe(filtered, use_container_width=True)

        csv = filtered.to_csv(index=False)
        st.download_button(
            "تحميل النتائج CSV",
            data=csv,
            file_name="grades_filtered.csv",
            mime="text/csv"
        )
    else:
        st.info("لا توجد نتائج مطابقة.")
