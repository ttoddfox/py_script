import os
import pandas as pd
import re
import warnings
import string
work_dir=r'C:\Users\txu1\Desktop'
warnings.filterwarnings('ignore')
import numpy as np
from fuzzywuzzy import fuzz
data_path=os.path.join(work_dir,'test_link2.xlsx')
data=pd.read_excel(data_path,encoding="utf-8",header=0,sheetname='CovDetailList')
web_path=os.path.join(work_dir,'commen_web.xlsx')
web=pd.read_excel(web_path,encoding="utf-8",header=0)

def clean_list(list1):
    list1=[x.lower() for x in list1 ]
    list1=[re.sub(r'[)|(]','',x) for x in list1]
    #list1=[re.sub(r'<.*?>', "", x) for x in list1]
    #print(list1)
    list2=[re.sub(r'''(\basset\b|\bmanagement\b|\blimited\b|\binvestment\b|\binvestments\b|\bltd\b|\bfund\b|\bllp\b|\bplc\b|\bgroups\b|managers
         |\bcapital\b|\bunit\b|\btrust\b|\blux\b|\bs.a.\b|\bmgt\b|\binv\b|\bmgmt\b|\bsa\b|\buk\b|\bpcc\b|\bllc\b|\bmanagers\b|\bfund\b|\bservices\b|\blife\b)''', "", x) for x in list1]
    list2=[x for x in list2 if x is not '']
    list2=[x for x in list2 if len(x)>1]
    return list2
print(len(data['InvestmentProvider']))
unique_list=np.unique(data['InvestmentProvider'])
provider_name=clean_list(web['provider name'])
web_link=web['website address']
data['link_address']=[np.nan]*data.shape[0]
#for i in range(len(data['InvestmentProvider'])):

for i in range(len(data['InvestmentProvider'])):
    if type(data['InvestmentProvider'][i])==str:
        temp_string=re.sub(r'\(.*?\)','',data['InvestmentProvider'][i] )  
        temp_list=temp_string.split()
        cleaned_list=clean_list(temp_list)
        after_string=" ".join(cleaned_list)
        #print(after_list)
        for j in range(len(web_link)):
            if type(after_string)==str and type(web_link[j])==str:
                pattern='\b'+after_string+'\b'
                if fuzz.ratio(after_string, provider_name[j])>80 or fuzz.partial_ratio(after_string, provider_name[j])>90 :
                    data.ix[i,'link_address']=provider_name[j]#change to list

'''

temp_data=pd.DataFrame({'name':unique_list})
temp_data['link_address']=[np.nan]*temp_data.shape[0]

for i in range(len(unique_list)):
        temp_string=re.sub(r'\(.*?\)','',unique_list[i] )  
        temp_list=temp_string.split()
        cleaned_list=clean_list(temp_list)
        after_string=" ".join(cleaned_list)
        after_string=re.sub(r'[)|(]','',after_string)#could approve      
        for j in range(len(provider_name)):
            if type(after_string)==str:
                pattern='\b'+after_string+'\b'
                if fuzz.partial_ratio(after_string, provider_name[j])>85 or re.search(pattern,provider_name[j]):
                    temp_data.ix[i,'link_address']=provider_name[j]
                #多个provider 选择建立list
#or fuzz.partial_ratio(after_string, web_link[j])>75:
#
temp_data.to_excel('link_result.xlsx')
'''
data.insert(9, 'link_address1',data['link_address'])
data.to_excel('link_result.xlsx')




        
