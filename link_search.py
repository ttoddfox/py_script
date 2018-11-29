import os
import pandas as pd
import re
import warnings
import string
from collections import Counter
import scipy.stats as stats
import pylab as pl

work_dir=r'C:\Users\txu1\Desktop'
warnings.filterwarnings('ignore')
import numpy as np
from fuzzywuzzy import fuzz
data_path=os.path.join(work_dir,'test_link2.xlsx')
data=pd.read_excel(data_path,encoding="utf-8",header=0,sheetname='CovDetailList')
web_path=os.path.join(work_dir,'commen_web.xlsx')
web=pd.read_excel(web_path,encoding="utf-8",header=0)

provider_name=web['provider name']
web_link=web['website address']
unique_list=np.unique(data['InvestmentProvider'])

temp_data=pd.DataFrame({'InvestmentProvider':unique_list})
temp_data['web_address']=['NaN']*temp_data.shape[0]



#### exact match used first string or first two strings
def match_list(list1,pro_name):
    pro_list=pro_name.split()
    if len(list1)>1 and len(pro_list)>1:
        temp_string1=list1[0]
        temp_string2=list1[0]+' '+list1[1]
        pro_name2=pro_list[0]+' '+pro_list[1]
        ratio1=fuzz.ratio(temp_string1, pro_list[0])
        ratio2=fuzz.ratio(temp_string2, pro_name2)
        max_ratio=max([ratio1,ratio2])
    else:
        temp_string1=list1[0]
        ratio1=fuzz.ratio(temp_string1, pro_list[0])
        max_ratio=ratio1
    return(max_ratio)

### primar clean string to delete speical characters.
def clean_list(string1):
    temp_list=string1.split()
    temp_list=[x.lower() for x in temp_list]
    temp_list=[re.sub(r'[^\w\s]','',x) for x in temp_list]
    temp_list=pd.Series(temp_list)
    cleaned_list=temp_list[~temp_list.isin(delete_list)]
    cleaned_list=list(cleaned_list)
    cleaned_string=" ".join(cleaned_list)
    return(cleaned_string)
##partio ratio for cleaned string 
for i in range(len(unique_list)):
    if type(unique_list[i])==str:
        temp_string=unique_list[i]
        temp_list=temp_string.split()       
        #print(after_list)
        for j in range(len(web_link)):
            temp_provider=provider_name[j]
            ratio=match_list(temp_list,temp_provider)
            if ratio>90:
                temp_data.ix[i,'web_address']=web_link[j]#change to list


### word count . frequency to get delete list
word_list=[]
for i in data['InvestmentProvider']:
    temp_list=i.split()
    temp_list=[x.lower() for x in temp_list]
    temp_list=[re.sub(r'[^\w\s]','',x) for x in temp_list]
    word_list=word_list+temp_list  
counts = Counter(word_list)
delete_list=[]
value_list=[]
for key,value in counts.items():
    value_list.append(value)
#calculate word count distribution get 90% as threshold
 
threshold = np.percentile(value_list, 90)
for key,value in counts.items():
    if value>threshold :
        delete_list.append(key)


second_clean_data=temp_data[temp_data['web_address']=='NaN']
second_clean_data=second_clean_data.reset_index(range(second_clean_data.shape[0]))
second_data_dim=second_clean_data.shape[0]
second_clean_data=second_clean_data.drop('index',1)


for i in range(second_data_dim):
        temp_string=second_clean_data.ix[i,'InvestmentProvider']
        cleaned_string=clean_list(temp_string)
        for j in range(len(provider_name)):
            temp_provider_name= provider_name[j]
            cleaned_provider=clean_list(temp_provider_name)
            if fuzz.ratio(cleaned_string,cleaned_provider)>80 or fuzz.partial_ratio(cleaned_string, cleaned_provider)>90 :
                second_clean_data.ix[i,'web_address']=web_link[j]#change to list
                
temp_data['web_address'] = second_clean_data.set_index('InvestmentProvider')['web_address'].combine_first(temp_data.set_index('InvestmentProvider')['web_address']).values

final_data=pd.merge(data,temp_data,how='outer',on='InvestmentProvider')
web=final_data['web_address']
final_data=final_data.drop(['web_address'],1)
final_data.insert(9,'web_address',web)

final_data=pd.read_csv('link_final.csv')
final_data.loc[final_data.web_address == 'NaN','web_address'] = np.nan

final_data.to_excel('link_final.xlsx')


        
