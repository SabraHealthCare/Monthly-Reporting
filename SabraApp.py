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
#---------------------------define parameters--------------------------
sheet_name_account_mapping="Account_Mapping"
sheet_name_entity_mapping="Property_Mapping"
bucket_mapping="sabramapping"

Sabra_detail_accounts_list=['PD_MCR_MGD_CARE','PD_MEDICARE','PD_COMM_INS', 'PD_PRIVATE', 'PD_MEDICAID', 'PD_VETERANS', 'PD_MCA_MGD_CARE', 'PD_OTHER','REV_MCR_MGD_CARE', 'REV_MEDICARE','REV_COMM_INS', 'REV_PRIVATE',
 'REV_MEDICAID', 'REV_VETERANS','REV_MCA_MGD_CARE', 'REV_MEDICARE_B','REV_OTHER', 'T_NURSING','T_DIETARY_RAW', 'T_DIETARY_OTHER','T_HOUSKEEPING', 'T_MAINTENANCE','T_MARKETING', 'T_BAD_DEBT','T_LEGAL', 'T_RE_TAX','T_INSURANCE', 
'T_GEN_ADMIN_OTHER','T_ANCILLARY_THERAPY', 'T_ANCILLARY_PHARMACY','T_ANCILLARY_OTHER', 'T_EXPENSES','T_MGMT_FEE', 'T_OTHER_OP_EXO','T_DEPR_AMORT', 'T_INT_INC_EXP','T_RENT_EXP', 'T_SL_RENT_ADJ_EXP','T_NURSING_LABOR', 'T_N_CONTRACT_LABOR',
 'T_OTHER_NN_LABOR', 'T_CASH_AND_EQUIV','T_AR_GROSS', 'T_AR_VAL_RES','T_INV', 'T_OTH_CUR_ASSETS','T_TRADE_PAY', 'T_OTHER_CUR_LIAB','T_LOC_OUT', 'T_OTHER_DEBT','T_CAPEX', 'T_AR_WRT_OFF','T_LOC_AVAIL', 'REV_ANCILLARY',
 'REV_CONT_ALLOW', 'T_NURSING_HOURS','T_N_CONTRACT_HOURS', 'T_OTHER_HOURS','G_REV_PRF', 'G_SEQ_SUSPENSION','G_FMAP_FUND', 'G_REV_EXTR_COVID','G_EXP_EXTR_COVID']

month_dic={1:["January","Jan","01/","1/","-1","-01","/1","/01"],2:["February","Feb","02/","2/","-2","-02","/2","/02"],3:["March","Mar","03/","3/","-3","-03","/3","/03"],4:["April","Apr","04/","4/","-4","-04","/4","/04"],5:["May","05/","5/","-5","-05","/5","/05"],6:["June","Jun","06/","6/","-06","-6","/6","/06"],\
           7:["July","Jul","07/","7/","-7","-07","/7","/07"],8:["August","Aug","08/","8/","-8","-08","/8","/08"],9:["September","Sep","09/","9/","-09","-9","/9","/09"],10:["October","Oct","10/","-10","/10",],11:["November","Nov","11/","-11","/11"],12:["December","Dec","12/","-12","/12"]}
year_dic={2021:["2021","21"],2022:["2022","22"],2023:["2023","23"],2024:["2024","24"],2025:["2025","25"],2026:["2026","26"],2019:["2019","19"],2018:["2018","18"],2020:["2020","20"]} 

dropdown_title_account='Map to Sabra Account'
dropdown_title_entity='Map sheet name to Property'  

Uploading_date=date.today()
Uploading_year=Uploading_date.year
Uploading_Lastyear=Uploading_year-1
Uploading_month=Uploading_date.month
Uploading_Lastyear
#------------------------------------functions------------------------------------
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
def get_row_no(dataset,row_header):
    return list(dataset.index).index(row_header)
def get_column_no(dataset,col_header):
    return list(dataset.columns).index(col_header)
def strip_lower_col(series_or_list):
    return(list(map(lambda x: str(x).strip().lower() if x==x else x,series_or_list)))
def strip_upper_col(series_or_list):
    return(list(map(lambda x: str(x).strip().upper() if x==x else x,series_or_list)))
    
def Upload_file_S3(file,bucket,filename):
    #s3 = boto3.client('s3')
    try:
        s3.upload_fileobj(file,bucket,"test/Jan/"+filename)
        st.success('File Successfully Uploaded')
        return True
    except FileNotFoundError:
        time.sleep(6)
        st.error('File wasn not uploaded.')
        return False 
     
#search tenant account column in P&L
# transfer all the account name(revenue, expense, occ) into lower case
# return col number of tenant account
sheet_name="Delaney_Creek_IS"
def Identify_Tenant_Account_Col(PL,mapping,sheet_name):
    for tenantAccount_col_no in range(0,PL.shape[1]):
        #trim and lower case column
        account_column=strip_lower_col(PL.iloc[:,tenantAccount_col_no])
        
        #find out how many tenant accounts match with mapping list
        match=[x in  list(account_column) for x in mapping["Tenant_account"]]

        #If 50% of accounts match with mapping list, identify this col as tenant account.
        if len(match)>0 and sum(x for x in match)/len(match)>0.1:
            return tenantAccount_col_no  
        else:
            # wrong account column,continue search accounts col
            continue
    
    # didn't find accounts col
    print("Can't find account column in sheet—— '"+sheet_name+"'")
        
#-------------------------------website widges---------------------------------
# drop down list of operator
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
uploaded_file = st.file_uploader(" ", type={"xlsx", "xlsm","xls"}, accept_multiple_files=False)
    
if uploaded_file:
    if uploaded_file.name[-5:]=='.xlsx':
        finicial_sheet_list=openpyxl.load_workbook(uploaded_file).sheetnames
        st.write(finicial_sheet_list)
    PL = pd.read_excel(uploaded_file,sheet_name =sheet_name)
    st.write(df)
    tenantAccount_col_no=Identify_Tenant_Account_Col(PL,mapping,sheet_name)
    st.write(tenantAccount_col_no)

    if st.button('Upload'):
        with st.spinner('Uploading...'):
            Upload_file_S3(uploaded_file,"sabramapping",uploaded_file.name)


   
                        
#if st.button('Run Checking'):
