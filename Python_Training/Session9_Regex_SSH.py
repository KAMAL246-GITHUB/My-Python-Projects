#!/usr/bin/env python
# coding: utf-8

# ## Regular Expressions in Python

# In[1]:


import re # import re packeage for all the regular expressions
#Refer a cheatsheet : https://www.debuggex.com/cheatsheet/regex/python


# In[2]:


### For practice random text was taken from here and there and put in a string variable named st

st = '''Python is a multi-paradigm, dynamically typed, multipurpose programming language.
It is designed to be quick (to learn, to use, and to understand), and to enforce a clean and uniform syntax.
Two similar but incompatible versions of Python are commonly in use, Python 2.7 and 3.x. 
For version-specific Python questions, add the [python-2.7] or [python-3.x] to This tag. 
When using a Python variant or library (e.g. Jython, PyPy, Pandas, Numpy), please include it in the tags

This session is to cover the basics of python. sample 33.5
The session mostly covers 3.X versions.
This is our chance to learn and share

If you have any questions you may write to SAHOO, KAMAL RANJAN (Enterprise Solutions) <KAMALRANJAN.SAHOO@rbs.com> or Pendse, Shankar (Enterprise Solutions) <Shankar.Pendse@rbs.co.uk>

Now lets talk about the SNOW items in Liquidity area. P3 incidents observed :

INC5273454	P3	Closed	Liquidity Position Store (LONDON)	1A system ( IGN/ANV/TMS) delivered late ...	1A system ( IGN/ANV/TMS) delivered late for cob07-02-2020	Liquidity Position Store (LONDON)	FT-Prod-RS-Liquidity	Indranil Roy Choudhury	Incident	
10-02-2020 07:18:10
8050464	
08-02-2020 04:43:12
Indranil Roy Choudhury	(empty)	(empty)	
		INC5307796	P3	Closed	Liquidity Position Store (LONDON)	There is Delay in Calv14 Batch Processin...	Delay in Calv14 Batch Processing	Liquidity Position Store (LONDON)	FT-Prod-RS-Liquidity	Praveen Gatta	Incident	
25-02-2020 07:16:01
8052524	
25-02-2020 07:00:01
Praveen Gatta	(empty)	(empty)	
		INC5295930	P3	Closed	Fire (LONDON)	Delay in LRI IGNLDN batch for COB 19 FEB...	Delay in LRI IGNLDN batch for COB 19 FEB2020 because of faulty trade issue at Fire end.	Liquidity Position Store (LONDON)	FT-Prod-RS-Liquidity	Praveen Gatta	Incident	
20-02-2020 04:53:50
7955051	
20-02-2020 08:50:00
Kamal Sahoo	(empty)	(empty)	
		INC5298906	P3	Closed	Liquidity Position Store (LONDON)	There is Delay in Calv14 Batch Processin...	Delay in Calv14 Batch Processing - JIRA LRI-2953	Liquidity Position Store (LONDON)	FT-Prod-RS-Liquidity	Kamal Kumar	Incident	
21-02-2020 06:52:46
7970803	
21-02-2020 07:00:00
Kamal Kumar	(empty)	(empty)	
		INC5258596	P3	Closed	Liquidity Position Store (LONDON)	GDS and IGN Batches delayed at SGL side ...	Delay in GDSLDN & IGNLDN Batch processing for COB 3rd FEB 2020	Liquidity Position Store (LONDON)	FT-Prod-RS-Liquidity	Murali Balakrishnan	Incident	
04-02-2020 04:11:26
8050266	
04-02-2020 07:00:00
Murali Balakrishnan	(empty)	(empty)	
		INC5253712	P3	Closed	GBM FT - SGL (LONDON)	Delay in Calypso feeds for COB 31st Jan ...	Delay in Calypso feeds for COB 31st Jan 2020	Liquidity Position Store (LONDON)	FT-Prod-RS-Liquidity	Shail Singhal	Incident	
01-02-2020 05:17:21
8020565	
01-02-2020 04:28:09
Shail Singhal	(empty)	(empty)	
		INC5255680	P3	Closed	GBM FT - SGL (LONDON)	Due to delay in SGL statnav readiness, G...	Delay in GDSLDN batch completion for COB 30th Jan 2020	Liquidity Position Store (LONDON)	FT-Prod-RS-Liquidity	Parasakthi Nagaraju	Incident	
03-02-2020 02:57:45
8066139	
31-01-2020 01:32:07
Parasakthi Nagaraju	(empty)	(empty)	
		INC5311136	P3	Closed	Liquidity Position Store (LONDON)	There is Delay in Calv14 Batch Processin...	Delay in Calv14 Batch Processing	Liquidity Position Store (LONDON)	FT-Prod-RS-Liquidity	Praveen Gatta	Incident	
26-02-2020 07:19:37
8052524	
26-02-2020 11:29:23
Praveen Gatta	(empty)	(empty)
INC5274151	P4	Closed	Liquidity Cognos (LONDON)	Cognos link: http://groupliquidityreport...	Multiple users facing issues with cognos web app functionality after VCS 3 migration	Liquidity Cognos (LONDON)	FT-Prod-RS-Liquidity	Indranil Roy Choudhury	Incident	
10-02-2020 10:34:53
8050464	
11-02-2020 03:22:04
Indranil Roy Choudhury	(empty)	(empty)	
		INC5274411	P4	Closed	Liquidity Cognos (LONDON)	Racfid- pandesz
Machine was moved to VC...	Request for Roll back of VCS3	Liquidity Cognos (LONDON)	FT-Prod-RS-Liquidity	Abhishek Yadav	Incident	
10-02-2020 11:40:33
8015066	
14-02-2020 09:38:56
Abhishek Yadav	(empty)	(empty)	
		INC5314671	P5	Closed	Liquidity Cognos (LONDON)	Log Space on Database: 'LONMS12894':'PMG...	lonmc01257 Log Space on Database: 'LONMS12894':'PMGBLQC01':'Cognos10' has: '93.00' percent used.	Liquidity Cognos (LONDON)	FT-Prod-RS-Liquidity	Parasakthi Nagaraju	Incident	
27-02-2020 12:41:32
tivoli	
02-03-2020 03:15:24
Tivoli Netcool Integration	(empty)	(empty)	
		INC5299557	P5	Closed	Liquidity Cognos (LONDON)	Job lqc.ldn.prd.2015lmderivcollateral.lp...	lqcpssis Job lqc.ldn.prd.2015lmderivcollateral.lp1 Failed.	Liquidity Cognos (LONDON)	FT-Prod-RS-Liquidity	Murali Balakrishnan	Incident	
21-02-2020 10:53:42
tivoli	
21-02-2020 16:27:23
Tivoli Netcool Integration	(empty)	(empty)	
		INC5309980	P5	Closed	Liquidity Position Store (LONDON)	HI Argon Team,

LPS is migrating to clou...	Request to add LPS application in Argon list to set password	Liquidity Position Store (LONDON)	FT-Prod-RS-Liquidity	Parasakthi Nagaraju	Incident	
25-02-2020 17:04:39
8066139	
03-03-2020 03:19:25
Parasakthi Nagaraju	(empty)	(empty)	
		INC5310864	P5	Closed	Liquidity Position Store (LONDON)	POLNLRI1 - Blocked session: SID 19 user ...	lonrs07296 POLNLRI1 - Blocked session: SID 19 user LPSBATCH blocked by 764 user LPSBATCH for over 30 mins on object	Liquidity Position Store (LONDON)	FT-Prod-RS-Liquidity	Murali Balakrishnan	Incident	
26-02-2020 04:34:17
tivoli	
26-02-2020 04:50:33
Tivoli Netcool Integration	(empty)	(empty)	

'''


# ### search()

# In[3]:


# This method Returns True if found and false if nto found

if re.search('Corona Virus',st):
    print ("Found")
else:
    print('Not Found')


# ### findall()

# In[4]:


# re.findall('This.*', st) #Display all the lines containing 'This'
# re.findall('[0-9][0-9]\.[0-9a-zA-Z]', st) #Display all the floating numbers in the format x.x
# re.findall('\(.*\)', st)
# re.findall('INC\d*', st) # Find all the incident number from junk
# re.findall('(INC\d*)\tP4', st) # Filter all the incident number followed by P4 or P5 or P3
re.findall('(INC\d*).*\((.*)\)', st) # Filter all the incident numbers and regions


# ### sub() Method to find and replace values

# In[5]:


re.sub('INC\d*','\*\*\*\*\*\*\*', st) 


# ### Greedy Matching

# In[6]:


st2 = 'From: Kamal: About: Python'
re.findall('^F.+:', st2) #Non Greedy matching 
re.findall('^F.+?:', st2) # Greedy Matching


# ## Connect to Linux/ Autosys

# In[ ]:


import sys
sys.path.insert(1, r'D:\Users\sahook\Desktop\Scripts\PYTHON3') # Using sys module and its insert method, insert the path of Credential.py file. Credential.py file in the given path stores the username and password etc. 
import Credential #import Credentialpy file
import paramiko #import paramiko module - it has methods to ssh a remote machine


# In[ ]:


ssh = paramiko.SSHClient() #Make SSH object
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(Credential.LPS_HOST, username=Credential.LPS_USERNAME, password=Credential.LPS_PASS, port=Credential.LPS_PORT) #Connect to the desired machine by using the credentials stored in Credential.py file
## In the lines below a command is executed using ssh.exec_command.
## The result is returned in the form of a tuple which contains 3 elements which are respectively assigned to stdin/stdout and stderr

# stdin, stdout, stderr = ssh.exec_command("ls -ltr <any directory>") #Connect to a remote linux machine and execute ls -ltr command
# stdin, stdout, stderr = ssh.exec_command('bash -c "source .my_profile; autorep -j flm%fxnldn%"')
stdin, stdout, stderr = ssh.exec_command(f'bash -c "source .my_profile; <script with absolute path> <argument>"')
lines = stdout.readlines() # Read the output into a variable called lines
errors = stderr.readlines() # Read the error into a variable called errors
body = ''.join(lines) # lines is a list separated by commas where each element ends with a new line. Join all the elements to make a single string so that it can be printed in a readable format.
print(body)
# print(errors)
ssh.close() # Close the Connection

