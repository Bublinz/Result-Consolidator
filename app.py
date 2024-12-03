import streamlit as st
import pandas as pd

st.title("Student Result Merger")
st.write("Upload your spreadsheet below:")

#upload file
test_file  = st.file_uploader("Upload Test Scores File", type=["xlsx"])
pratical_file  = st.file_uploader("Upload Practical Scores File", type=["xlsx"])
exam_file  = st.file_uploader("Upload Exam Scores File", type=["xlsx"])

if test_file and pratical_file and  exam_file:
    #Load files into dataframes
    test_score = pd.read_excel(test_file)
    practical_score = pd.read_excel(pratical_file)
    exam_score = pd.read_excel(exam_file)
    st.write("Files upload successfully!")



    
