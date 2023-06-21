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

def Get_Year(single_string):
    if single_string!=single_string or single_string==None or type(single_string)==float:
        return 0,""
    else:
        for Year in year_dic.keys():
            for Year_keyword in year_dic[Year]:
                if Year_keyword in single_string:
                    return Year,Year_keyword
        return 0,""

def Get_Month_Year(single_string):
    if single_string!=single_string or single_string==None or type(single_string)==float:
        return 0,0
    if type(single_string)==datetime:
        return int(single_string.month),int(single_string.year)
    
    single_string=str(single_string)
    Year,Year_keyword=Get_Year(single_string)
    
    # remove year from string
    single_string=single_string.replace(Year_keyword,"")
 
    for Month in month_dic.keys() :#[01,02,03...12]
        for  Month_keyword in month_dic[Month]: #["Jan","January","01","-1","/1",'1/']
            if Month_keyword.lower() in single_string.lower():
                remaining=single_string.lower().replace(Month_keyword.lower(),"").replace("/","")\
                                .replace("-","").replace(" ","").replace("_","")

                #if there are more than 3 other char in the string, this string maybe not the date 
                if len(remaining)>=3:
                    return 0,0
                else:   
                    return Month,Year
            # only year without month, length>3
            else:
                continue
    return 0,Year      

def Month_continuity_check(month_list):
    inv=[]
    month_list=list(filter(lambda x:x!=0,month_list))
    if len(month_list)==0:
        return False
    else:
        inv=[int(month_list[month_i+1])-int(month_list[month_i]) for month_i in range(len(month_list)-1) ]
        if  len(set(inv))<=2 and all([x in [1,-1,11,-11] for x in set(inv)]):
            #continues month, it is month row
            return True
        else:
            return False

def Year_continuity_check(year_list):
    inv=[]
    year_list=list(filter(lambda x:x!=0,year_list))
    if len(year_list)==0:
        return False
    else:
        inv=[int(year_list[year_i+1])-int(year_list[year_i]) for year_i in range(len(year_list)-1) ]
        if len(set(inv))<=2 and all([x in [1,0,-1] for x in set(inv)]):
            #continues year, it is year row
            return True        
        else:
            return False
# add year to month_header: identify current year/last year giving a list of month

def Add_year_to_header(month_list):
    available_month=list(filter(lambda x:x!=0,month_list))
    
    today=date.today()
    current_year= today.year
    last_year=today.year-1

    if len(available_month)==1:
        
        if datetime.strptime(available_month[0]+"/01/"+current_year,'%m/%d/%Y').date()<today:
            year=current_year
        else:
            year=today.year-1
        return year
     
    year_change=0     
    # month decending  #and available_month[0]<today.month
    if (available_month[0]>available_month[1] and available_month[0]!=12) or \
    (available_month[0]==1 and available_month[1]==12) : 
        date_of_assumption=datetime.strptime(str(available_month[0])+"/01/"+str(current_year),'%m/%d/%Y').date()
        if date_of_assumption<today and date_of_assumption.month<today.month:
            report_year_start=current_year
        elif date_of_assumption>=today:
            report_year_start=last_year
        for i in range(len(available_month)):
            available_month[i]=report_year_start-year_change
            if i<len(available_month)-1 and available_month[i+1]==12:
                year_change+=1
            
    # month ascending   
    elif (available_month[0]<available_month[1] and available_month[0]!=12) \
        or (available_month[0]==12 and available_month[1]==1): #and int(available_month[-1])<today.month
        date_of_assumption=datetime.strptime(str(available_month[-1])+"/01/"+str(current_year),'%m/%d/%Y').date()    
        if date_of_assumption<today:
            report_year_start=current_year
        elif date_of_assumption>=today:
            report_year_start=last_year
        for i in range(-1,len(available_month)*(-1)-1,-1):
   
            available_month[i]=report_year_start-year_change
            if i>len(available_month)*(-1) and available_month[i-1]==12:
                #print("year_change",year_change)
                year_change+=1
    
    else:
        return False
 
    j=0
    for i in range(len(month_list)):
        if month_list[i]!=0:
            month_list[i]=available_month[j]
            j+=1

    return month_list  

# find the Month/year row and return row number
def Identify_Month_Row(PL,tenantAccount_col_no,sheet_name):
    PLrow=PL.shape[0]
    PLcol=PL.shape[1]
    row_size=min(20,PLrow)
    month_table=pd.DataFrame(0,index=range(row_size), columns=range(PLcol))
    year_table=pd.DataFrame(0,index=range(row_size), columns=range(PLcol))
    
    for row_i in range(min(20,PLrow)):
        for col_i in range(PLcol):
            if type(PL.iloc[row_i,col_i])==int or type(PL.iloc[row_i,col_i])==float:
                continue
            month_table.iloc[row_i,col_i],year_table.iloc[row_i,col_i]=Get_Month_Year(PL.iloc[row_i,col_i])
    year_count=[]
    month_count=[]
    max_len=0
    for row_i in range(row_size):
        valid_month=list(filter(lambda x:x!=0,month_table.iloc[row_i,]))
        valid_year=list(filter(lambda x:x!=0,year_table.iloc[row_i,]))
        month_count.append(len(valid_month))
        year_count.append(len(valid_year))

    # didn't find any month in all the rows
    if all(map(lambda x:x==0,month_count)):
        print("Can't identify month/year columns in sheet——'"+sheet_name+"'")   
        return [0],0
    month_sort_index = np.argsort(np.array(month_count))
    year_sort_index = np.argsort(np.array(year_count))
    for month_index_i in range(-1,-4,-1): # only check three of the most possible rows
        
        #month_sort_index[-1] is the index number of month_count in which has max month count
        #month_sort_index[i] is also the index/row number of finicial
        
        #print(month_count[month_sort_index[month_index_i]])
        if month_count[month_sort_index[month_index_i]]>1:
            #check validation of month
            #print(Month_continuity_check(month_table.iloc[month_sort_index[month_index_i],]))
            if Month_continuity_check(month_table.iloc[month_sort_index[month_index_i],]):
                for year_index_i in range(-1,-4,-1):
                    # check validation of year
                    if Year_continuity_check(year_table.iloc[year_sort_index[year_index_i],]) \
                        and year_count[year_sort_index[year_index_i]]==month_count[month_sort_index[month_index_i]]:
                       
                        PL_date_header=year_table.iloc[year_sort_index[year_index_i],].apply(lambda x:str(int(x)))+\
                        month_table.iloc[month_sort_index[month_index_i],].apply(lambda x:"" if x==0 else "0"+str(int(x)) if x<10 else str(int(x)))
                        return PL_date_header,month_sort_index[month_index_i]
                    
                    # all the year rows are not valid, add year to month
                    else:
                        continue
                    # all the year rows are not valid, add year to month
                year_table.iloc[year_sort_index[year_index_i],]=Add_year_to_header(list(month_table.iloc[month_sort_index[month_index_i],]))
                PL_date_header=year_table.iloc[year_sort_index[year_index_i],].apply(lambda x:str(int(x)))+\
                month_table.iloc[month_sort_index[month_index_i],].apply(lambda x:"" if x==0 else "0"+str(int(x)) if x<10 else str(int(x)))
                
                st.write("Missing year in date header in sheet '"+sheet_name+"'. Filled year as below: ")
                st.write(list(filter(lambda x:str(x)!='0',financial_date_header)))
                return PL_date_header,month_sort_index[month_index_i]
                        
            # month is not continuous, check next one
            else:
                continue
                
        # only one month in header:month and year must exist for one month header
        elif month_count[month_sort_index[month_index_i]]==1:
            # month and year must match 
            st.write("There is only one month in sheet——'"+sheet_name+"'")
            col_month=0
            #find the col number of month
            while(month_table.iloc[month_sort_index[month_index_i],col_month]==0):
                col_month+=1
                
                #if month_table.iloc[month_sort_index[index_i],col_month]!=1:
                #if column of month is smaller than column of account, or there is no year in month, continue 
            if col_month<tenantAccount_col_no or year_table.iloc[month_sort_index[month_index_i],col_month]==0:
                st.write("There is no year in date row in sheet——'"+sheet_name+"'")
                continue
           
            count_num=0
            count_str=0
            for row_month in range(month_sort_index[month_index_i],financial.shape[0]):
                if financial.iloc[row_month,col_month]==None or pd.isna(financial.iloc[row_month,col_month]) or financial.iloc[row_month,col_month]=="":
                    continue

                elif type(financial.iloc[row_month,col_month])==float or type(financial.iloc[row_month,col_month])==int:
                    count_num+=1
                else:
                    count_str+=1
                # count_num/str is count of numous/character data under month
                # for a real month column, numous data is supposed to be more than character data
            if count_str>0 and count_num/count_str<0.8:
                continue
                
            else:
                financial_date_header=year_table.iloc[month_sort_index[month_index_i],].apply(lambda x:str(int(x)))+\
                        month_table.iloc[month_sort_index[month_index_i],].apply(lambda x:"" if x==0 else "0"+str(int(x)) if x<10 else str(int(x)))
                        
                return financial_date_header,month_sort_index[month_index_i]
    st.write("Can't identify date row in P&L for sheet: '"+sheet_name+"'")
    return [0],0
st.write(Identify_Month_Row(PL,tenantAccount_col_no,sheet_name))
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
   
    

st.subheader("Upload P&L:")
uploaded_file = st.file_uploader(" ", type={"xlsx", "xlsm","xls"}, accept_multiple_files=False)
    
if uploaded_file:
    if uploaded_file.name[-5:]=='.xlsx':
        finicial_sheet_list=openpyxl.load_workbook(uploaded_file).sheetnames
        
    PL = pd.read_excel(uploaded_file,sheet_name =sheet_name)
    tenantAccount_col_no=Identify_Tenant_Account_Col(PL,mapping,sheet_name)
   

    if st.button('Upload'):
        with st.spinner('Uploading...'):
            Upload_file_S3(uploaded_file,"sabramapping",uploaded_file.name)


   
                        
#if st.button('Run Checking'):
