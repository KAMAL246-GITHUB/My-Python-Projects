#!/usr/bin/env python
# coding: utf-8

# ## File Operations, WITH Clause, OS module

# #### Create/ write a file

# In[ ]:


fh = open('Sample.txt','w')
fh.write('''This is a sample file.
This is being created to learn the basics of file operation in python.
The intent is to automate many manaul tasks, going forward.
''')
fh.close()


# #### Append to an existing a file

# In[ ]:


fh = open('Sample.txt','a')
fh.write(
'''
We have already created this file.
Now we are just appending to test if the data is looking fine.
That confirms the append mode.
''')
fh.close()


# #### Read the file

# In[ ]:


fh = open('Sample.txt', 'r')
# fr = fh.read() #Read all the file in one string
fl = fh.readlines()
for line in fl:
    print (line)
# print(fr)   
fh.close()


# #### Delete the file

# In[ ]:


import os
try:
    os.remove('Sample.txt')
    print ('File deleted')
except:
    print ('The file does not exist')


# #### Use of context manager : with clause

# In[ ]:


with open('Sample.txt', 'r') as fh:
    print (fh.read())
    
# with open('Sample.txt','a') as fh:
#     fh.write('''This is another line i want to append to.
#     And this is the next line''')


# ### Task / Worked Example: 

# #### Below piece of code creates a file with a list of pseudo production job names. They are are from various regions. Using file operations and context manager concept, create 3 new files where you store the jobs connected to LDN, MNH & ASP regions respectively.

# In[ ]:


with open('job.txt','w') as fh:
    fh.write(
        '''
        a
        b
        c
        ''')

