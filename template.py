import os
import pandas as pd
work_dir=r'C:\Users\txu1\Desktop'
import numpy as np
data_path=os.path.join(work_dir,'final_result1.csv')
data=pd.read_csv(data_path,encoding="gb18030",header=0)
print(data.columns)
#temp_df=data[['SecID','URL/FileName']]
#temp_df=temp_df.drop_duplicates()

column_list=['Document Type','SecID','ISIN','CUSIP','FileURL','FileName'
             'Format','Effective Date(yyyy/mm/dd/)','language','FixURL(Y/N)'
             ,'Market','Document Title','Announcement Category',
             'InternalOnly(Y/N)','CompanyID','Currency','SelectType']
final_df=pd.DataFrame(columns=column_list)
final_df=final_df[['Document Type','SecID','ISIN','CUSIP','FileURL','FileName'
             'Format','Effective Date(yyyy/mm/dd/)','language','FixURL(Y/N)'
             ,'Market','Document Title','Announcement Category',
             'InternalOnly(Y/N)','CompanyID','Currency','SelectType']]


grouped=data.groupby('URL/FileName')
grouped_dict=grouped.groups
final_df_row_count=0
for key,value in grouped_dict.items():
    grouped_dict[key].values
    temp_df=data.loc[grouped_dict[key].values]
    temp_df=temp_df.reset_index(drop=True)
    new_sec_id=''
    for i in temp_df['SecID']:
        new_sec_id=new_sec_id+str(i)+','
    new_sec_id=new_sec_id[:-1]
    final_df=final_df.append(temp_df.loc[0])
    final_df=final_df.reset_index(drop=True)
    final_df.ix[final_df_row_count,'SecID']=new_sec_id
   
    final_df_row_count+=1
final_df['FileURL']=final_df['URL/FileName']
final_df['FileName']=final_df['title']
final_df['Format']='PDF'
final_df['language']='Chinese'
final_df['Market']='China'
final_df['SelectType']='Fund'
print(final_df)
final_df.to_csv('template.csv')
#input("\n\nPress the enter key to exit.")
