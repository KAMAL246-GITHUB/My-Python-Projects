import concurrent.futures as cf # Module for Multithreading in python
import paramiko # Module for SSH to conenct to Linux from Windows
import time
import Credential # Import Credentials.py where the credential to connect Oracle DB or other machines are stored
import re # Module for regex
import cx_Oracle # Module to connect oracle DB
import numpy as np
import pandas as pd
from  matplotlib import pyplot as plt
import copy #To perform deep copy or shallow copy
import Task_Trending as TT # Task_Trending.py file sotores the functions which connect to respective DB, fetch data and plot them. 
%matplotlib inline # Magic function used to display the charts in specific style "%matplotlib notebook" can be used too
import ETA_SQL as ES # ETA_SQL.py stores the SQLs which may be used by the script to fetch data from DB

# The class below stores color codes in varibales to be used later for display. Particularly useful in Jupyter. May not work on all the platforms in similar way
#Sample usage : print(color.BOLD + color.RED + color.UNDERLINE  +'Hello ALL !' + color.END)
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

start=time.perf_counter() # Note the start time so that in the end, duration of script execution can be calculated 

def get_autosys_details(js):
    '''
    This function takes the job stream name as argument, Connects to a linux machine via SSH. It executes a shell script 
    where the job stream is passed as an argument. The shell script checks the autosys boxes corresponding to that stream 
    and all its dependencies and returns the status which are further stored in the dictionary defined before. The function 
    finally returns the dictionary's key value pair where key is the stream which was passed into and value is what status 
    was returned by the shell script
    '''
    ssh = paramiko.SSHClient() # Create SSH object
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # Add missing key policy
    ssh.connect(Credential.LPS_HOST, username=Credential.LPS_USERNAME, 
                password=Credential.LPS_PASS, port=Credential.LPS_PORT) # Connect to Linux machine using the SSH object's connect method
    stdin, stdout, stderr = ssh.exec_command\
    (f'bash -c "source .my_profile; /home/sahook/scripts/shell_scripts/ThreadLRI_SOD_Check.sh {js}"') #Execute the shell script after loading the desired profile
    lines = stdout.readlines() # Stores the output returned by the shell script
    errors = stderr.readlines() # Stores the errors returned (if any while executing the shell script)
    body = ''.join(lines) # Format the shell script out put to make it more readable
    dic[f'{js}'] = body 
    ssh.close() #Close the ssh connection
    return (dic[f'{js}'])

dic = {} #Create an empty dictionary
streams = ['syxldn','gfxldn','gfxmnh','gfxsng','iceldn','ecoldn','calv14','tmsldn','fxnldn','rrsldn',
           'wsnldn','wsrmnh','wsrasp','wsrldn','wsuroi','wsufac','wsunir','wsgldn','calasp','calmnh',
           'calldn','anvldn','gdsldn','gdsmnh','lqsldn','ignldn'] # List of all LRI streams in lower case letters as the shell script needs them in lower case

#Trigger the scripts for multiple streams in multiple threads
with cf.ThreadPoolExecutor() as ex:
    results = ex.map(get_autosys_details,streams) # By mapping the function and the list of streams, it is ensured that the function runs in multiple threads for multiple streams 
    
st_comp="" # Declare empty string and append the completed streams to this later.
st_pending="" # Declare empty string and append the pending streams to this later.

# Keep on appending the values to st_comp and st_pending
for val in dic.values():
    if " completed at " in val:
        st_comp += val
    else:
        st_pending += val
        
# Print headers via below two lines        
print (color.BOLD + color.GREEN + "COMPLETED STREAMS\n*****************\n"+ color.END + st_comp)
print (color.BOLD + color.RED + "PENDING STREAMS\n*****************\n"  + color.END + st_pending)

LRI_STREAMS = re.findall('Stream.* (.*) machine1',st_pending) # Create a list of LRI job streams which are pending (based on machine name)
FDM_STREAMS = re.findall('Stream.* (.*) machine2',st_pending) # Create a list of FDM job streams which are pending
LRI_STREAMS = ["%"+i+"%" for i in LRI_STREAMS if (i.startswith('FLM_') and '_RRSLDN' not in i ) ] #Exclude RRSLDN as its graph can not be generated as of now

############## Plot the data and show the pending stream status ############
[TT.get_LRIstream_runtime(i)  for i in LRI_STREAMS] # Call the respective function from TaskTending.py file for the pending LRI streams
[TT.get_FDMstream_runtime(i)  for i in FDM_STREAMS] # Call the respective function from TaskTending.py file for the pending FDM streams

############## Print the data in tabular format ##############
pd.options.mode.chained_assignment = None # To ignore chained assignement warning - Try not using this line and rather follow the instructions given in the error
df = pd.DataFrame(list(dic.items()), columns = ['Stream', 'Time']) # Make a data frame
df['Stream']= df['Stream'].str.upper() #Change the stream names to Upper case 
df_complete = df[df['Time'].str.contains('completed at')]
df_pending = df[~df['Time'].str.contains('completed at')]
df_complete['Time'] = df_complete['Time'].str.extract('.*( [0-9]{2}:[0-9]{2}).*') # Extract time from the date stamp using regext
df_pending['Status']  = df_pending['Time'].str.extract('\n.*\n(.*)') # extract status using regex
df_pending.drop(columns='Time', inplace = True)
df_pending.reset_index(drop=True)
print (color.BOLD + color.RED + "PENDING STREAMS\n*****************"  + color.END)
display (df_pending.reset_index(drop = True))
print (color.BOLD + color.GREEN + "\nCOMPLETED STREAMS\n*****************"+ color.END )
display (df_complete)


############## Print time taken by the script ##############
end=time.perf_counter()
print(f'The script took {end-start} Seconds')   

