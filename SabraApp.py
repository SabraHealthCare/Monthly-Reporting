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
from openpyxl import load_workbook
import openpyxl
import xlrd
import warnings
import streamlit as st
from st_files_connection import FilesConnection
import boto3
sheet_name_account_mapping="Account_Mapping"
sheet_name_entity_mapping="Property_Mapping"
bucket_mapping="sabramapping"

s3 = boto3.client('s3')
obj = s3.get_object(Bucket=bucket_mapping, Key="Operator_list.xlsx")
operator_list = pd.read_excel(obj['Body'].read(), sheet_name='Operator_list')


st.title("Sabra HealthCare Reporting App")
st.subheader("Operator name:")
operator= st.selectbox(
    ' ',(operator_list))

if operator != 'select operator':
    mapping_path="Mapping/"+operator+"/"+operator+"_Mapping.xlsx"
    mapping=Read_Account_Mapping()
    st.write(mapping)
    


st.subheader("Upload P&L:")
uploaded_file = st.file_uploader(" ", type={"xlsx", "xlsm"}, accept_multiple_files=False)


# get account mapping 
def Read_Account_Mapping():
    #read mapping format
    obj = s3.get_object(Bucket=bucket_mapping, Key=mapping_path)
    format = pd.read_excel(obj['Body'].read(), sheet_name=sheet_name_account_mapping,header=0)
        #convert tenant_account to lower case
    format["Tenant_account"]=strip_lower_col(format["Tenant_account"])
    format["Sabra_second_account"]=strip_upper_col(format["Sabra_second_account"])
    format["Sabra_account"]=strip_upper_col(format["Sabra_account"])
        # remove nan in col Sabra_account
    mapping=format.loc[list(map(lambda x:x==x,format["Sabra_account"])),\
                                     ["Sabra_account","Tenant_account","Sabra_second_account"]]
    mapping=mapping.loc[list(map(lambda x:x==x,mapping["Tenant_account"])),\
                                     ["Sabra_account","Tenant_account","Sabra_second_account"]]
    mapping=mapping.drop_duplicates()
    mapping=mapping.reset_index(drop=True)
    return mapping
    
def Upload_file_S3(file,bucket,filename):
    s3 = boto3.client('s3')
    try:
        s3.upload_fileobj(file,bucket,"test/Jan/"+filename)
        st.success('File Successfully Uploaded')
        return True
    except FileNotFoundError:
        time.sleep(6)
        st.error('File wasn not uploaded.')
        return False     



if uploaded_file:
    df = pd.read_excel(uploaded_file,sheet_name ="Delaney_Creek_IS")
    st.write(df)
    wb = openpyxl.load_workbook(uploaded_file)
    st.write(wb.sheetnames)
    if st.button('Upload'):
        with st.spinner('Uploading...'):
            Upload_file_S3(uploaded_file,"sabramapping",uploaded_file.name)
        
       
                        
#if st.button('Run Checking'):
