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
#from prettytable import PrettyTable
import streamlit as st
#warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)
#from openpyxl.utils.dataframe import dataframe_to_rows

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
#df=pd.read_excel("https://sabrahealthcare-my.sharepoint.com/:x:/r/personal/sli_sabrahealth_com/_layouts/15/Doc.aspx?sourcedoc=%7BCD8B9C15-464C-4B33-8583-D8D776617AD4%7D&file=Main_Report.xlsx&action=default&mobileredirect=true")
#st.write(df)
DATA_URL = (
    "https://sabrahealthcare-my.sharepoint.com/personal/sli_sabrahealth_com/_layouts/15/guestaccess.aspx?docid=1cd8b9c15464c4b338583d8d776617ad4&authkey=Aa8j07B1ANILhEn-y2KyrUU&e=eJZf31"
)

@st.cache(persist=True)
def load_data(DATA_URL):
    data = pd.read_excel(DATA_URL)
    return data
data = load_data(DATA_URL)
st.write(data)
def save_uploadedfile(uploadedfile,address):
     with open(address+uploadedfile.name,"wb") as f:
         f.write(uploadedfile.getbuffer())
     return st.success(uploadedfile.name +" saved")

st.subheader("Upload P&L:")
uploaded_file = st.file_uploader(" ", type={"xlsx", "xls","xlsm"}, accept_multiple_files=False)

template_path="C://Users//Sha Li//Desktop//Uploading project//"+operator+"//"
financial_path="C://Users//Sha Li//Desktop//Uploading project//"+operator+"//"

if uploaded_file: 
    file_details = {"FileName":uploaded_file.name,"FileType":uploaded_file.type}
    #df = pd.read_excel(uploaded_file)
    save_uploadedfile(uploaded_file,financial_path)



st.write(
        "By default, this P&L is for 2023 May reporting. "
        )
st.write("[Learn More >](https://sabrahealthcare.sharepoint.com/)")

#if st.button('Run Checking'):
#    main(template_path_filename,finical_path_filename)

