import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Student Grades Viewer", layout="wide")

st.image("logo.png", width=180)
st.title("Student Grades Table")

DATA_PATH = Path("grades.xlsx")

def load_data():
    if not DATA_PATH.exists():
        return None
    try:
        df = pd.read_excel(DATA_PATH)
        return df
    except:
        return None

df = load_data()

if df is None:
    st.error("Data file not found.")
else:
    search_by = st.radio("Search by:", ["ID", "Name"])
    query = st.text_input("Enter search value:")

    student_name_col = "الاسم"
    student_id_col = "رقم الطالب"
    parent_col = "رقم ولي الامر"

    fixed_cols = [student_name_col, student_id_col, parent_col]
    grade_cols = [c for c in df.columns if c not in fixed_cols]

    final_df = pd.DataFrame()
    final_df["Student Name"] = df[student_name_col]
    final_df["Student ID"] = df[student_id_col]
    final_df["Parent Number"] = df[parent_col]

    for col in grade_cols:
        final_df[col] = df[col]

    if query:
        if search_by == "ID":
            results = final_df[final_df["Student ID"].astype(str).str.contains(query, na=False)]
        else:
            results = final_df[final_df["Student Name"].astype(str).str.contains(query, case=False, na=False)]

        if not results.empty:
            st.success(f"{len(results)} result(s) found")
            st.dataframe(results, use_container_width=True)

            csv = results.to_csv(index=False)
            st.download_button(
                label="Download Results (CSV)",
                data=csv,
                file_name="results.csv",
                mime="text/csv"
            )
        else:
            st.info("No results found.")
    else:
        st.dataframe(final_df, use_container_width=True)
