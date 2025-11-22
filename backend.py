# backend.py
import pandas as pd
from pathlib import Path

DATA_PATH = Path("grades.xlsx")

def load_grades():
    if not DATA_PATH.exists():
        return None
    try:
        df = pd.read_excel(DATA_PATH)

        # تجهيز الأعمدة الأساسية بافتراض وجودها في الجدول
        required_cols = ["الاسم", "رقم_الطالب", "رقم_ولي_الامر"]

        # تأكد إن الأعمدة موجودة
        for col in required_cols:
            if col not in df.columns:
                raise ValueError(f"العمود '{col}' غير موجود في الملف!")

        # ترتيب الأعمدة
        other_cols = [c for c in df.columns if c not in required_cols]
        df = df[required_cols + other_cols]

        return df
    except Exception as e:
        print(f"Error: {e}")
        return None
