import streamlit as st
import pandas as pd
import io
from openpyxl import load_workbook

st.title("Student Result Consolidator")

#upload file
exam_file  = st.file_uploader("Upload Exam Scores File", type=["xlsx"])

if  exam_file:
    #Load the Exam spreadsheet using openpyxl
    ogr_template = load_workbook(exam_file)

    Sheet1 = ogr_template['Sheet1']
    st.write("Files upload successfully!")




    
