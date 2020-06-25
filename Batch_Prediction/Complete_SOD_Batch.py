import concurrent.futures as cf
import paramiko
import time
import Credential
import re
import cx_Oracle
import numpy as np
import pandas as pd
from  matplotlib import pyplot as plt
import copy
import Task_Trending as TT

%matplotlib inline

import ETA_SQL as ES


class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

#print(color.BOLD + color.RED + color.UNDERLINE  +'Hello ALL !' + color.END)

start=time.perf_counter()

def get_autosys_details(js):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(Credential.LPS_HOST, username=Credential.LPS_USERNAME, 
                password=Credential.LPS_PASS, port=Credential.LPS_PORT)
    stdin, stdout, stderr = ssh.exec_command\
    (f'bash -c "source .my_profile; /home/sahook/scripts/shell_scripts/ThreadLRI_SOD_Check.sh {js}"')
    lines = stdout.readlines()
    errors = stderr.readlines()
    body = ''.join(lines)
    dic[f'{js}'] = body
    ssh.close()
    return (dic[f'{js}'])

dic = {}
streams = ['syxldn','gfxldn','gfxmnh','gfxsng','iceldn','ecoldn','calv14','tmsldn','fxnldn','rrsldn',
           'wsnldn','wsrmnh','wsrasp','wsrldn','wsuroi','wsufac','wsunir','wsgldn','calasp','calmnh',
           'calldn','anvldn','gdsldn','gdsmnh','lqsldn','ignldn']

#Trigger the scripts for multiple streams in multiple threads
with cf.ThreadPoolExecutor() as ex:
    results = ex.map(get_autosys_details,streams)
    
st_comp=""
st_pending=""

for val in dic.values():
    if " completed at " in val:
        st_comp += val
    else:
        st_pending += val
print (color.BOLD + color.GREEN + "COMPLETED STREAMS\n*****************\n"+ color.END + st_comp)
print (color.BOLD + color.RED + "PENDING STREAMS\n*****************\n"  + color.END + st_pending)

LRI_STREAMS = re.findall('Stream.* (.*) ecpvm005239',st_pending)
FDM_STREAMS = re.findall('Stream.* (.*) lon-tdwprd-app',st_pending)
LRI_STREAMS = ["%"+i+"%" for i in LRI_STREAMS if (i.startswith('FLM_') and '_RRSLDN' not in i ) ]

############## Plot the data and show the pending stream status ############
[TT.get_LRIstream_runtime(i)  for i in LRI_STREAMS]
[TT.get_FDMstream_runtime(i)  for i in FDM_STREAMS]

############## Print time taken by the script ##############
end=time.perf_counter()
print(f'The script took {end-start} Seconds')   
