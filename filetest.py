
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
                        try:
                                PdfFileReader(pdf_path)
                                

                        except:
                            print(pdf_path)
                            os.remove(pdf_path)
                if filename.endswith('htm') or filename.endswith('html'):
                    print(dirpath,filename)
                    remove_path=os.path.join(dirpath,filename)
                    #os.remove(remove_path)
                if filename.endswith('crdownload'):
                    print(dirpath,filename)






                
    

