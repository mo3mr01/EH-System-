if not results.empty:
    st.success(f"تم العثور على {len(results)} نتيجة/نتائج")

    for index, row in results.iterrows():
        st.markdown("---")

        # عنوان الطالب في المنتصف
        st.markdown(
            "<h3 style='text-align: center; color:#2c70d3;'>🎓 بيانات الطالب</h3>",
            unsafe_allow_html=True
        )

        # ---- جدول الطالب (تصغير + محاذاة يمين + RTL) ---- #
        row_df = pd.DataFrame(row).rename(columns={index: "القيمة"})
        row_df.index.name = "البند"
        row_df = row_df.reset_index()

        # Container صغير في النص
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
