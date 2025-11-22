import streamlit as st
import pandas as pd

st.set_page_config(page_title="كشف درجات الطلاب", layout="wide")

# -------- تحميل البيانات --------
file_path = "/mnt/data/كشف درجات الطلاب.xlsx"
df = pd.read_excel(file_path)

st.title("📘 كشف درجات الطلاب")

# -------- عرض الطالب كـ Card --------
for idx, row in df.iterrows():
    with st.container():
        st.markdown(
            """
            <div style="
                border: 2px solid #444;
                border-radius: 12px;
                padding: 20px;
                margin-bottom: 20px;
                direction: rtl;
                font-size: 18px;
            ">
            """,
            unsafe_allow_html=True
        )

        # الصف العلوي: الاسم + الجروب
        st.markdown(
            f"""
            <table style="width:100%; text-align:center; border-collapse: collapse;">
                <tr>
                    <th style="border:1px solid #000; padding:10px;">اسم الطالب</th>
                    <th style="border:1px solid #000; padding:10px;">الجروب</th>
                </tr>
                <tr>
                    <td style="border:1px solid #000; padding:10px;">{row['اسم']}</td>
                    <td style="border:1px solid #000; padding:10px;">{row['جروب']}</td>
                </tr>
            </table>
            """,
            unsafe_allow_html=True
        )

        # الصفوف العمودية يمين
        st.markdown(
            f"""
            <table style="width:100%; text-align:center; border-collapse: collapse; margin-top:15px;">
                <tr>
                    <th style="width:30%; border:1px solid #000; padding:10px;">رقم الطالب</th>
                    <td style="border:1px solid #000; padding:10px;">{row['رقم الطالب']}</td>
                </tr>

                <tr>
                    <th style="border:1px solid #000; padding:10px;">رقم ولي الأمر</th>
                    <td style="border:1px solid #000; padding:10px;">{row['رقم ولي الأمر']}</td>
                </tr>

                <tr>
                    <th style="border:1px solid #000; padding:10px;">درجات الشهر الأول</th>
                    <td style="border:1px solid #000; padding:10px;">{row['شهر1_امتحان1']} - {row['شهر1_امتحان2']} - {row['شهر1_امتحان3']} - {row['شهر1_امتحان4']}</td>
                </tr>

                <tr>
                    <th style="border:1px solid #000; padding:10px;">درجات الشهر الثاني</th>
                    <td style="border:1px solid #000; padding:10px;">{row['شهر2_امتحان1']} - {row['شهر2_امتحان2']} - {row['شهر2_امتحان3']} - {row['شهر2_امتحان4']}</td>
                </tr>
            </table>
            """,
            unsafe_allow_html=True
        )

        st.markdown("</div>", unsafe_allow_html=True)
