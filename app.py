import streamlit as st
import pandas as pd
from pathlib import Path

DATA_PATH = Path("grades.xlsx")

@st.cache_data(ttl=60)
def load_data(path):
    try:
        df = pd.read_excel(path, engine="openpyxl")
        return df
    except Exception as e:
        st.error(f"خطأ في قراءة الملف: {e}")
        return None

st.title("📚 Student Grades Viewer")

df = load_data(DATA_PATH)

if df is not None:
    search_by = st.radio("البحث بواسطة:", ["ID", "الاسم"])
    query = st.text_input("اكتب ID أو الاسم هنا:")

    if query:
        if search_by == "ID":
            try:
                qnum = float(query)
                results = df[df.iloc[:,0] == qnum]
            except:
                results = df[df.iloc[:,0].astype(str).str.contains(query, na=False)]
        else:
            results = df[df.iloc[:,1].astype(str).str.contains(query, case=False, na=False)]

        if not results.empty:
            st.success(f"تم العثور على {len(results)} نتيجة/نتائج")
            st.dataframe(results, use_container_width=True)
        else:
            st.info("لا توجد نتائج للبحث.")
else:
    st.warning("ملف البيانات غير موجود.")
