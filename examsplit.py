import streamlit as st
import pandas as pd
import openpyxl
import os
from io import BytesIO

def exam_split():
    st.title("Exam Sheet Splitter")
    st.write("Upload an Excel file with multiple sheets, and extract specific columns for each sheet.")

    # File uploader for the exam file
    exam_file = st.file_uploader("Upload your exam Excel file (.xlsx):", type=["xlsx"])


    # Streamlit title and description
    st.title("Exam File Splitter")
    st.write("Upload an Excel file with multiple sheets, and the system will extract specific columns and save each sheet as a separate file.")

    # File uploader for the exam file
    exam_file = st.file_uploader("Upload your exam Excel file (.xlsx):", type=["xlsx"])

    if exam_file:
        try:
            # Load the Excel file
            workbook = pd.ExcelFile(exam_file)
            sheets = workbook.sheet_names  # Get all sheet names

            st.write(f"**Sheets detected:** {', '.join(sheets)}")

            # Prepare for download
            output_zip = BytesIO()  # To store files in memory
            skipped_sheets = []  # Track skipped sheets
            processed_sheets = {}  # Track processed sheets with row counts

            for sheet_name in sheets:
                # Read the sheet starting from row 15
                data = pd.read_excel(workbook, sheet_name=sheet_name, header=None, skiprows=14)

                # Check if column C (3rd column) is empty
                if data.shape[1] < 3 or data.iloc[:, 2].dropna().empty:
                    skipped_sheets.append(sheet_name)
                    continue

                # Extract specific columns by position
                extracted_data = data.iloc[:, [1, 2, 7, 8, 10, 13]]  # B, C, H, I, K, N

                # Drop rows where all selected columns are empty
                extracted_data.dropna(how='all', inplace=True)

                # Save the sheet data to an in-memory file
                output_file = BytesIO()
                with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
                    extracted_data.to_excel(writer, sheet_name=sheet_name, index=False, header=False)

                # Add the in-memory file to a dictionary for download
                processed_sheets[sheet_name] = output_file.getvalue()

            # Provide results summary
            st.write("### Processing Summary")
            st.write(f"**Total number of Department(s):** {len(processed_sheets)}")
            st.write(f"**Skipped records due to error:** {len(skipped_sheets)}")
            if skipped_sheets:
                st.write(f"**Skipped Department:** {', '.join(skipped_sheets)}")

            # Provide download buttons for processed sheets
            for sheet_name, file_data in processed_sheets.items():
                st.download_button(
                    label=f"Download {sheet_name}.xlsx",
                    data=file_data,
                    file_name=f"{sheet_name}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )

        except Exception as e:
            st.error(f"An error occurred: {e}")
