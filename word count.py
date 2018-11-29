import os
import pandas as pd
import re
import warnings
import string
from collections import Counter
work_dir=r'C:\Users\txu1\Desktop'
#warnings.filterwarnings('ignore')
import numpy as np
from fuzzywuzzy import fuzz
data_path=os.path.join(work_dir,'test_link2.xlsx')
data=pd.read_excel(data_path,encoding="utf-8",header=0,sheetname='CovDetailList')
web_path=os.path.join(work_dir,'commen_web.xlsx')
web=pd.read_excel(web_path,encoding="utf-8",header=0)

print(data.head())
print(len(data['InvestmentProvider']))
provider_name=web['provider name']
web_link=web['website address']
data['link_address']=[np.nan]*data.shape[0]
unique_list=np.unique(data['InvestmentProvider'])

temp_data=pd.DataFrame({'InvestmentProvider':unique_list})
temp_data['link_address']=['NaN']*temp_data.shape[0]
print(unique_list)

word_list=[]
for i in unique_list:
    temp_list=i.split()
    print(temp_list)
    word_list=word_list+temp_list
counts = Counter(word_list)
print(counts)

