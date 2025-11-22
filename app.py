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

# ----------- إعداد الصفحة -----------
st.set_page_config(layout="wide")

# ----------- اللوجو في المنتصف -----------
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    st.image("logo.png", width=200)
    st.markdown("</div>", unsafe_allow_html=True)


# ----------- العنوان -----------
st.markdown(
    "<h1 style='text-align: center; margin-top: -20px;'> English House Student Data Viewer </h1>",
    unsafe_allow_html=True
)

df = load_data(DATA_PATH)

# ----------- محتوى الصفحة -----------
if df is not None:

    # البحث في منتصف الصفحة
    colA, colB, colC = st.columns([1, 2, 1])
    with colB:
        search_by = st.radio("البحث بواسطة:", ["ID", "الاسم"], horizontal=True)
        query = st.text_input("اكتب ID أو الاسم هنا:")

    if query:
        # البحث حسب ID أو الاسم
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

            for index, row in results.iterrows():
                st.markdown("---")

                # عنوان بيانات الطالب
                st.markdown(
                    "<h3 style='text-align: center; color:#2c70d3;'>🎓 بيانات الطالب</h3>",
                    unsafe_allow_html=True
                )

                # تجهيز البيانات كجدول
                row_df = pd.DataFrame(row).rename(columns={index: "Value"})
                row_df.index.name = "Cloumn"
                row_df = row_df.reset_index()

                # جدول صغير في المنتصف
                table_col1, table_col2, table_col3 = st.columns([1, 2, 1])
                with table_col2:

                    # تنسيق RTL
                    st.markdown("""
                    <style>
                        .rtl-table {
                            direction: rtl;
                            text-align: right;
                            font-size: 16px;
                        }
                    </style>
                    """, unsafe_allow_html=True)

                    st.markdown('<div class="rtl-table">', unsafe_allow_html=True)
                    st.table(row_df)
                    st.markdown('</div>', unsafe_allow_html=True)

        else:
            st.info("لا توجد نتائج للبحث.")

else:
    st.warning("ملف البيانات غير موجود.")


