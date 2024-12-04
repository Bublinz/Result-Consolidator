import streamlit as st
import pandas as pd
import io

st.title("Student Result Merger")
st.write("Upload your spreadsheet below:")

#upload file
test_file  = st.file_uploader("Upload Test Scores File", type=["xlsx"])
lab_file  = st.file_uploader("Upload Lab Scores File", type=["xlsx"])
exam_file  = st.file_uploader("Upload Exam Scores File", type=["xlsx"])

#if test_file and lab_file and  exam_file:
if exam_file:
    #Load files into dataframes
    test_score = pd.read_excel(test_file)
    Lab_score = pd.read_excel(lab_file)
    exam_scores = pd.read_excel(exam_file)
    st.write("Files upload successfully!")

# Merge Logic
# if exam_file:
if test_file and lab_file and exam_file:

#Clean and renamme columns
    test_score.rename(columns={'Reg No': 'RegNo'}, inplace=True)
    Lab_score.rename(columns={'Reg No': 'RegNo'}, inplace=True)
    exam_scores.rename(columns={'MATRIC NO': 'RegNo'}, inplace=True)

    # # Combine name fields in exam_scoress
    # st.write("Test Scores File Preview:")
    # st.dataframe(test_score.head(20))

    
    # Proceed with processing
    exam_scores['Candidates Name'] = (exam_scores['SURNAME'] + " " + exam_scores['FIRSTNAME'] + " " + exam_scores['MIDDLENAME'])
    exam_scores[['Candidates Name', 'RegNo', 'EXAM SCORE']]

    # Merge dataframes
    merged_data = pd.merge(test_score, Lab_score, on='RegNo', how='outer')
    final_result = pd.merge(merged_data, exam_scores, on='RegNo', how='outer')

    #Reoder columns
    final_result = final_result[['Candidates Name', 'RegNo', 'TEST', 'LAB', 'EXAM SCORE']]

    # Remove rows where Registration Number is missing
    final_result = final_result[final_result['Candidates Name'].notna()]

    # Drop rows where all score columns are empty
    final_result = final_result.dropna(subset=['TEST', 'LAB', 'EXAM SCORE'], how='all')


    st.write("Result Consolidation Successful!")
    st.dataframe(final_result)

# Download merged result as excel

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer: final_result.to_excel(writer, index=False, sheet_name='Results') 
    output.seek(0),
    st.download_button(
        label="Download Excel File", 
        data=output,
        file_name= "ABC.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )