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


Now lets talk about the SNOW items in Liquidity area. P3 incidents observed :

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

