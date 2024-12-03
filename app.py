import streamlit as st
import pandas as pd

st.title("Student Result Merger")
st.write("Upload your spreadsheet below:")

#upload file
test_file  = st.file_uploader("Upload Test Scores File", type=["xlsx"])
lab_file  = st.file_uploader("Upload Lab Scores File", type=["xlsx"])
exam_file  = st.file_uploader("Upload Exam Scores File", type=["xlsx"])

if test_file and lab_file and  exam_file:
    #Load files into dataframes
    test_score = pd.read_excel(test_file)
    Lab_score = pd.read_excel(lab_file)
    exam_score = pd.read_excel(exam_file)
    st.write("Files upload successfully!")

# Merge Logic
if test_file and lab_file and exam_file:

#Clean and renamme columns
    test_score.renamme(columns={'Reg. no': 'RegNo'}, inplace=True)
    Lab_score.renamme(columns={'Reg. no': 'RegNo'}, inplace=True)
    exam_score.renamme(columns={'MATRIC NO': 'RegNo'}, inplace=True)

    # Combine name fields in exam_scores
    exam_score['Name'] = (exam_score['SURNAME'] + "" + exam_score['FIRSTNAME'] + "" + exam_score['MIDDLENAME'])
    exam_score[['RegNo', 'Name', 'Exam']]

    # Merge dataframes
    merged_data = pd.merge(test_score, Lab_score, on='RegNo', how='outer')
    final_result = pd.merge(merged_data, exam_score, on='RegNo', how='outer')

    #Reoder columns
    final_result = final_result[['S/N', 'Name', 'RegNo', 'Test', 'Lab_score', 'Exam']]
    st.write("Result Consoolidation Successful!")
    st.dataframe(final_result)





    
