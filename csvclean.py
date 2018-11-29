import warnings
warnings.filterwarnings('ignore')
#-*- encoding=utf-8 -*-

import os
from math import isnan
import pandas as pd
import math
import os
import re
import numpy as np
import sys
import xlrd
import csv


def csv_from_excel(excel_file,csv_file):

    wb = xlrd.open_workbook(excel_file)
    sh = wb.sheet_by_name('Sheet1')
    your_csv_file = open(csv_file, 'wb')
    wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

    for rownum in xrange(sh.nrows):
        wr.writerow(sh.row_values(rownum))

    your_csv_file.close()


def insert_english_row(row_index,df):
    df1=df.loc[:row_index]
    df2=df.loc[row_index+1:]
    for i in range(row_index+1,row_index+5):
            df1.loc[i]=list([np.nan]*data.shape[1])
    result_df=pd.concat([df1,df2],ignore_index=True)
    return(result_df)

def insert_row(row_index,df):
    df1=df.loc[:row_index]
    df2=df.loc[row_index+1:]
    df1.loc[row_index+1]=df1.loc[row_index]
    df1.ix[row_index+1,'db_indicator']=0
    result_df=pd.concat([df1,df2],ignore_index=True)
    return(result_df)

def fill_row(row_index,df):
    for i in range(row_index+1,row_index+5):
        df.ix[row_index,'Announcement']=announcement_list[0]
        if pd.notnull(df.loc[i].all):
            df.loc[i]=df.loc[row_index]
            df.ix[i,'Announcement']=announcement_list[i-row_index]
            
    return(df)



work_dir=r'C:\Users\txu1\Desktop\china_daily'
file=os.listdir(work_dir)
for i in file:
    if i.startswith('china'):
        target=i
'''
excel_file=os.path.join(work_dir,target)
print(excel_file)
csv_file=re.sub(target,'xlsx','csv')
csv_file=os.path.join(work_dir,csv_file)
csv_from_excel(excel_file,csv_file)
'''

data_path=os.path.join(work_dir,target)
web_fund_path=os.path.join(work_dir,'web_fund.csv')
skip_fund_path=os.path.join(work_dir,'skip_fund.csv')





data=pd.read_excel(data_path,encoding="gb2312",header=0)
data=data.dropna(thresh=2)
comment_list=data['Comments']
comment_list=np.array(comment_list)
English_list=[]
data['Announcement']=list([np.nan]*data.shape[0])
announcement_list=['Share Sale Announcement','Rulebook/Statutes',
                   'Rule book summary','Custodian Agreement','Prospectus']
for i in range(data.shape[0]):
        temp_comment=comment_list[i]      
        if type(temp_comment)==float and isnan(temp_comment):
            continue                   
        if re.search('[a-zA-Z]',temp_comment):
            #print(temp_comment)#english need add 4 row
            English_list.append(temp_comment)
        if temp_comment=="基金经理":
            double_add_begin_index=i
         
data=data.reset_index(range(data.shape[0]))
for double_index in range(double_add_begin_index+1,data.shape[0]):
        temp_comment=comment_list[double_index]
        try :
                isnan(temp_comment)

        except:
                double_end_index=double_index
                break

data['db_indicator']=np.zeros(data.shape[0])
for i in range(double_add_begin_index,double_end_index):
        data.ix[i,'db_indicator']=1


for i in range(len(data.index)):
        if data.ix[i,'db_indicator']==1:
                data=insert_row(i,data)
                data.ix[i,'Announcement']='Prospectus'
                data.ix[i+1,'Announcement']='Summary Prospectus'
                    
data=data.drop('db_indicator',1)
for i in English_list:
    temp_index=data[data['Comments']==i].index.tolist()
    temp_index=temp_index[0]
    data=insert_english_row(temp_index,data)

for i in English_list:
    temp_index=data[data['Comments']==i].index.tolist()
    temp_index=temp_index[0]
    data=fill_row(temp_index,data)  


#clear exists fund name
share_list=data['Share Name']
skip_fund=pd.read_csv(skip_fund_path,encoding="gb2312")
skip_fund_list=skip_fund['fund_name']
web_fund=pd.read_csv(web_fund_path,encoding="gb2312")


data['skip_indicator']=[np.nan]*(data.shape[0])
data['link_address']=[np.nan]*(data.shape[0])
skip_fund_list=[re.sub(' ','',x) for x in skip_fund_list]
for i in range(len(share_list)):
    if type(share_list[i])!=float:
        temp_fundname=share_list[i][0:2]
        temp_fundname1=share_list[i][0:3]
        temp_fundname2=share_list[i][0:4]
        temp_fundname3=share_list[i][0:5]
        for fund_name in skip_fund_list:
            if temp_fundname==fund_name or temp_fundname1==fund_name  or temp_fundname2==fund_name or temp_fundname3==fund_name:
                data.ix[i,'skip_indicator']=1
        for j in range(len(web_fund['fund'])):
            if temp_fundname==web_fund['fund'][j] or temp_fundname1==web_fund['fund'][j] or temp_fundname2==web_fund['fund'][j] or temp_fundname3==fund_name:
                data.ix[i,'link_address']=web_fund['link'][j]


for i in range(data.shape[0]):
    if type(data.ix[i,'Announcement'])!=str and isnan(data.ix[i,'Announcement']):
        data.ix[i,'Announcement']='announcement'

#print(data.columns)
data['URL/FileName']=[np.nan]*data.shape[0]
data['title']=[np.nan]*data.shape[0]

data=data[['Process Date','SecID','Share Name','Comments','Resource','URL/FileName','title','Announcement','skip_indicator','link_address']]
data.to_excel(os.path.join(work_dir,'temp_result.xlsx'),encoding='gb2312')

input("\n\nPress the enter key to exit.")


    
        
        
   



