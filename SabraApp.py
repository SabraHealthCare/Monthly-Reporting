
import pandas as pd
from pandas import ExcelWriter
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import statistics
import os
import xlwt
from xlwt.Workbook import *
import xlsxwriter
import matplotlib.ticker as mtick
import pyodbc
import numpy as np
from calendar import monthrange
import sys
from datetime import datetime, timedelta
from datetime import date
#from itertools import compress
from os import walk
#from openpyxl import load_workbook
import openpyxl
import xlrd
import warnings
import streamlit as st
from st_files_connection import FilesConnection




st.title("Sabra HealthCare Reporting App")
st.subheader("Operator name:")
operator= st.selectbox(
    ' ',
    ("Advanced Recovery Systems",
"Affinity",
"Andrew Residence",
"Atrium Health",
"Aurora",
"Avalon",
"Avalon Realty",
"Avamere Family",
"Avista",
"Baybridge",
"Baylor Scott & White",
"Bear Mountain",
"Brickyard",
"Cadia",
"Celebration",
"Chai",
"Civitas",
"Claiborne",
"CommuniCare",
"Consulate",
"Covenant Care",
"Discovery",
"Dwight",
"EBS",
"EHG",
"Emerald",
"EmpRes Healthcare",
"Encore",
"Enlivant",
"Ensign",
"Epic Group",
"Focused Post Acute",
"Forest Park",
"Fox",
"Fundamental",
"Genesis",
"Golden Living",
"Haven",
"Health Systems",
"Health_Dimension",
"Healthmark Group",
"Holiday",
"Ignite",
"Inspirit Senior Living",
"Landmark Recovery",
"Legacy Living",
"LeoBrownGroup",
"LifeHouse",
"Lifes Journey",
"Magnolia Health Sys",
"Maison",
"Marlin Spring - Excelsoins",
"Marlin Spring - Spring Living",
"Maxwell Group",
"Meridian",
"Meridian Health Care",
"National Healthcare",
"NeuroRestorative",
"New Dawn",
"New Haven",
"New Orange Hills",
"Nexion Health Mgmt",
"Nexus Systems",
"NMS",
"No Relationship",
"North Shore",
"Nye",
"Oakbrook",
"Paradigm",
"Parkside",
"Pathways",
"Peregrine",
"RCA",
"ResCare HomeCare",
"Retirement Living",
"RoseCastle",
"Saber",
"Sacred Heart",
"Salem Villages",
"Senior Care Centers",
"Shelbourne",
"Sienna",
"Signature Behavioral",
"Signature Healthcare",
"Sinceri Senior Living",
"Solvere",
"Southern Admin",
"Southern Healthcare",
"Southwest LTC",
"Spectrum Healthcare",
"Spring Hills",
"Stoney River",
"Sundara",
"Tenet",
"The McGuire Group",
"Titan",
"Trinity",
"TRMC",
"Tryko Partners",
"Vibra Healthcare",
"Vivra",
"Wachusett Ventures",
"Welcov Healthcare",
"Wingate Healthcare"))
#("/"+uploadedfile.name


conn = st.experimental_connection('s3', type=FilesConnection)
df = conn.read("sabramapping/test.csv", input_format="csv", ttl=600)
st.write(df)



def save_uploadedfile(uploadedfile,directory):
     with open(directory+uploaded_file.name,"wb") as f:
         f.write(uploadedfile.getbuffer())
     return st.success(uploadedfile.name +" saved")


st.subheader("Upload P&L:")
uploaded_file = st.file_uploader(" ", type={"xlsx", "xls","xlsm"}, accept_multiple_files=False)

if uploaded_file: 
    file_detail = {"FileName":uploaded_file.name,"FileType":uploaded_file.type}
    df = pd.read_excel(uploaded_file)
    save_uploadedfile(uploaded_file,"")


st.write( "By default, this P&L is for 2023 May reporting. ")
st.write("[Learn More >](https://sabrahealthcare.sharepoint.com/)")

#if st.button('Run Checking'):
#    main(template_path_filename,finical_path_filename)



    
import boto3



uploaded_mp4 = st.file_uploader("Select an MP4 file")
if uploaded_mp4 is not None:
                st.success(uploaded_mp4.name + ' Selected')
                #bytes_data = uploaded_mp4.getvalue()
                if st.button('Upload'):
                    with st.spinner('Uploading...'):
                        s3 = boto3.client('s3')
    
 
                        with open("test2.xlsx", 'wb') as data:
                            s3.upload_fileobj(uploaded_mp4, bucket, "lUU1C5GLW59BoQTEpy4OUb5xsH48QRo0hYOGFtEb")
                        #s3.upload_file(file, bucket, s3_file)
                        st.success('File Successfully Uploaded')
