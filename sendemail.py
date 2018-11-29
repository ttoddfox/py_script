import win32com.client as win32
import psutil
import os
import subprocess
from size import formatSize
from size import get_directory_size
import string
import zipfile

def ziplist(zip_list, ziph):
    for file in zip_list:
        for subroot, subdirs, subfiles in os.walk(os.path.join(work_dir,file)):
            for subfile in subfiles:
                ziph.write(os.path.join(subroot, subfile),os.path.join(file,subfile))

def send_email(attachment_file,subject,send_to_address):
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = send_to_address#mail.To = 'abc@xzs.com; bhm@ert.com',
    #mail.CC=
    mail.Subject = subject
    mail.body = """Hi all,

this is tesing message
                   


best regards,
Tod Xu
 """
    mail.Attachments.Add(attachment_file)
    mail.send
        
def open_outlook():
    try:
        subprocess.call(["C:\Program Files (x86)\Microsoft Office\root\Office16\OUTLOOK.EXE"])
        os.system("C:\Program Files (x86)\Microsoft Office\root\Office16\OUTLOOK.EXE");
    except:
        print("Outlook didn't open successfully")


work_dir=r'C:\Users\txu1\Desktop\5.3 task'
start_list=list(string.ascii_lowercase)

sub_dir=os.listdir(work_dir)
file_dict={}
file_dict=file_dict.fromkeys(start_list)

for key, value in file_dict.items():
    file_dict[key]=[]
    for i in sub_dir:
        i=i.lower()
        if i.startswith(key):
            file_dict[key].append(i)
print(file_dict)

for key,value in file_dict.items():
    temp_list=file_dict[key]
    if len(temp_list)>0:
        zipf = zipfile.ZipFile(r'C:\Users\txu1\Desktop\zip\msdocupload_'+key+'.zip', 'w', zipfile.ZIP_DEFLATED)
        ziplist(temp_list, zipf)
        zipf.close()
        

# Checking if outlook is already opened. If not, open Outlook.exe and send email
for item in psutil.pids():
    p = psutil.Process(item)
    if p.name() == "OUTLOOK.EXE":
        flag = 1
        break
    else:
        flag = 0

if (flag == 1):
    print(1)
    #send_email()
else:
    open_outlook()
    #send_email()
             
attachment1 = r"C:\Users\txu1\Desktop\5.3 task\Smith % willimianson\smith & williamson 4"
size=get_directory_size(attachment1)

print(formatSize(size))
