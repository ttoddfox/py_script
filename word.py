
import win32com.client
import os
import sys
import re
from os import listdir
import comtypes.client
wdFormatPDF = 17
work_dir=r'C:\Users\txu1\Desktop\word'
data_path=os.path.join(work_dir,'138386808289.docx')
#in_file = os.path.abspath(sys.argv[1])
out_file = os.path.join(work_dir,'test.pdf')
word = win32com.client.Dispatch('Word.Application')
word.Visible = False
doc = word.Documents.Open(data_path)
count=0
for p in doc.Paragraphs:
    print(p)
    count=count+1
    if count>20:
        break
    

doc.SaveAs(out_file, FileFormat=wdFormatPDF)
doc.Close()
word.Quit()
