import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import win32com.client
import json
import time 
from time import sleep
import numpy as np
import os
import datetime
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from math import isnan
from fuzzywuzzy import fuzz

#-*- encoding=utf-8 -*-
work_dir=r'C:\Users\txu1\Desktop'
page_num=7

page_list=range(1,page_num)
url_list=[]
link_df=pd.DataFrame(columns=['web_link','title'])
data_path=os.path.join(work_dir,'test_result.csv')
data=pd.read_csv(data_path,encoding='gb2312')
missing_index_list=[]

for i in range(data.shape[0]):
    if type(data.ix[i,'title'])!=str and type(data.ix[i,'URL/FileName']!=str):
        missing_index_list.append(i)

for i in page_list:
    temp_location='http://www.cgbchina.com.cn/noticeNew.gsp?pageNum=%(page)d' %{'page':i}
    url_list.append(temp_location)
for i in url_list:
    web = requests.get(i)  
    web.encoding='gb2312'
    soup = BeautifulSoup(web.text, 'html.parser')
    title_list=soup.find_all(class_='articleList')
    #parent=title_list[0].parent
    #print(parent.find_all('li'))
    title_list1=soup.find_all(title=re.compile('(.*?)'),href=re.compile('/noticeNewDetail*'))
    for i in title_list1:
        temp_link='http://www.cgbchina.com.cn'+i['href']
        temp_title=i['title']
        temp_df=pd.DataFrame({'web_link':temp_link,
                          'title':temp_title},index=[0])
        link_df=pd.concat([link_df,temp_df])
link_df=link_df.reset_index(range(link_df.shape[0]))
link_df.to_csv('link_df.csv')
'''
link_df=pd.read_csv('link_df.csv',encoding='gb2312')
data['missing_link']=[np.nan]*data.shape[0]
title_list=link_df['title']
for i in missing_index_list:
    temp_share_name=data.ix[i,'Share Name']
    for j in range(len(title_list)):
        #print(title_list[j])
        if fuzz.partial_ratio(temp_share_name, title_list[j])>60:
 
            data.ix[i,'missing_link']=link_df.ix[j,'web_link']
data.to_csv('test_link.csv')

test_url='http://www.cgbchina.com.cn/noticeNewDetail.gsp?symbol=004655&id=747591'
web = requests.get(test_url)  
web.encoding='gb2312'
soup = BeautifulSoup(web.text, 'html.parser')
parent=soup.find_all(class_='textContent')[0].parent
title=parent.h3.contents

f=open('test.txt','w')
'test.txt'.encode('gbk','ignore')
word = win32com.client.Dispatch('Word.Application')
word.Visible = False

out_file = os.path.join(work_dir,'test.pdf')
wdFormatPDF = 17
input_file=os.path.join(work_dir,'test.docx')
doc = word.Documents.Open(input_file)

for i in range(len(parent.p.contents)): 
    line='%(content)s\r\n'%{'content':str(parent.p.contents[i])}
    line=line.replace('<br/>','')
    #print(line)
    f.write(line)
    
    
doc.SaveAs(out_file, FileFormat=wdFormatPDF)    
doc.Close()
word.Quit()
f.close()
'''
