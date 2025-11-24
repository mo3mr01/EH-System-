import streamlit as st
import pandas as pd
from pathlib import Path

DATA_PATH = Path("grades.xlsx")

# ----------- قراءة البيانات -----------
@st.cache_data(ttl=60)
def load_data(path):
    try:
        # dtype=str يضمن كل الخلايا تتحول لنص لتسهيل البحث
        df = pd.read_excel(path, engine="openpyxl", dtype=str)
        return df
    except Exception as e:
        st.error(f"خطأ في قراءة الملف: {e}")
        return None

# دالة مساعدة لتنظيف الـ id/قيمة البحث
def normalize_id(x):
    if pd.isna(x):
        return ""
    s = str(x).strip()
    # لو Excel حط رقم بصيغة 123.0 إزالة .0 لأن أحياناً يظهر هكذا بعد التحويل
    if s.endswith('.0'):
        s = s[:-2]
    return s

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

    # اختر اسم عمود الـ ID لو موجود، وإلا استخدم العمود الأول
    id_col = "ID" if "ID" in df.columns else df.columns[0]
    name_col = "الاسم" if "الاسم" in df.columns else (df.columns[1] if len(df.columns) > 1 else df.columns[0])

    # البحث في منتصف الصفحة
    colA, colB, colC = st.columns([1, 2, 1])
    with colB:
        search_by = st.radio("البحث بواسطة:", ["ID", "الاسم"], horizontal=True)
        query = st.text_input("اكتب ID أو الاسم هنا:")

    if query:
        q_clean = query.strip()
        if search_by == "ID":
            # نطبع الأعمدة كـ strings ونطابق بعد التنظيف
            df_ids = df[id_col].astype(str).apply(normalize_id)
            q_norm = normalize_id(q_clean)

            # هنا نعمل تطابق تام أولاً، وإذا ما في نتائج نستخدم contains كـ fallback
            exact_mask = df_ids == q_norm
            if exact_mask.any():
                results = df[exact_mask]
            else:
                contains_mask = df_ids.str.contains(q_norm, na=False)
                results = df[contains_mask]
        else:
            # بحث الاسم غير حساس لحالة الحروف
            results = df[df[name_col].astype(str).str.contains(q_clean, case=False, na=False)]

        # عرض النتائج
        if not results.empty:
            st.success(f"تم العثور على {len(results)} نتيجة/نتائج")
            for index, row in results.iterrows():
                st.markdown("---")
                st.markdown(
                    "<h3 style='text-align: center; color:#2c70d3;'>بيانات الطالب/ة 👨‍🏫</h3>",
                    unsafe_allow_html=True
                )
                row_df = pd.DataFrame(row).rename(columns={index: "Value"})
                row_df.index.name = "Features"
                row_df = row_df.reset_index()

                table_col1, table_col2, table_col3 = st.columns([1, 2, 1])
                with table_col2:
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
