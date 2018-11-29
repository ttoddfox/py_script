
from PyPDF2 import PdfFileReader
import os
import sys
import re

location=str(sys.argv[1])
work_dir=r'C:\Users\txu1\Desktop'
work_dir=os.path.join(work_dir,location)
print(work_dir)



for dirpath, dirnames, filenames in os.walk(work_dir):
	for filename in filenames:
                pdf_path=os.path.join(dirpath,filename)
                #print(pdf_path)
                if pdf_path.endswith('pdf'):
                        pdf_content=''
                        num_pages=2
                        pdf=PdfFileReader(pdf_path)
                        for i in range(0, num_pages):
                                pdf_content += pdf.getPage(i).extractText() + "\n"
                                pdf_content = " ".join(pdf_content.replace(u"\xa0", " ").strip().split()) 
                                isin=pdf_content.find('ISIN')
                                if isin !=None:
                                        print(pdf_content[isin:isin+15])
