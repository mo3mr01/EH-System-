import streamlit as st
import pandas as pd
from pathlib import Path

DATA_PATH = Path("grades.xlsx")

# ----------- قراءة البيانات -----------
@st.cache_data(ttl=60)
def load_data(path):
    try:
        df = pd.read_excel(path, engine="openpyxl")
        return df
    except Exception as e:
        st.error(f"خطأ في قراءة الملف: {e}")
        return None


# ----------- تنسيق الصفحة -----------
st.set_page_config(layout="wide")

# ----------- اللوجو في المنتصف -----------
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.image("logo.png", width=180)

st.markdown("<h1 style='text-align: center;'>📚 Student Grades Viewer</h1>", unsafe_allow_html=True)

df = load_data(DATA_PATH)

# ----------- محتوى الصفحة -----------
if df is not None:

    # البحث في المنتصف
    colA, colB, colC = st.columns([1,2,1])
    with colB:
        search_by = st.radio("البحث بواسطة:", ["ID", "الاسم"], horizontal=True)
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

        # لو في نتائج
        if not results.empty:
            st.success(f"تم العثور على {len(results)} نتيجة/نتائج")

            # عرض كل نتيجة في جدول منفصل
            for index, row in results.iterrows():
                st.markdown("---")
                st.markdown(
                    "<h3 style='text-align: center; color:#2c70d3;'>🎓 بيانات الطالب</h3>",
                    unsafe_allow_html=True
                )
                st.table(pd.DataFrame(row).rename(columns={index: "المعلومات"}))

        else:
            st.info("لا توجد نتائج للبحث.")

else:
    st.warning("ملف البيانات غير موجود.")
