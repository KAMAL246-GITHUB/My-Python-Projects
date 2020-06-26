#!/usr/bin/env python
# coding: utf-8

# ### Import libraries

# In[2]:


import pandas as pd
import cx_Oracle as  CO #import cx_Oracle Package for DB operations
import sys
sys.path.insert(1, r'D:\Users\sahook\Desktop\Scripts\PYTHON3') #Includes this path in the default paths to be refered while looking for any python module
import Test_Credentials as TC # import Test_Credentials.py file located in the path above


# ## How to make a Pandas dataframe

# #### 1: Creating Pandas DataFrame from lists of lists.

# In[3]:


# initialize list of lists 
data = [['Python', 9], ['Java', 8], ['C++', 7]] 
  
# Create the pandas DataFrame 
df1 = pd.DataFrame(data, columns = ['Language', 'Rating']) 
  
# print dataframe. 
df1


# #### 2: Creating DataFrame from Dictionary of narray/lists
# ##### To create DataFrame from dict of narray/list, all the narray must be of same length. If index is passed then the length index should be equal to the length of arrays.  If no index is passed, then by default, index will be range(n) where n is the array length.
# 

# In[4]:


# intialise data of lists. 
data = {'Genre':['Thriller', 'Drama', 'Romance', 'Animation'], 
        'Movies':['Fight Club', 'Titanic', 'When Harry Met Sally', 'Lion King'], 
        'Rating':[8,9,8.5,8]} 
  
# Create DataFrame 
df = pd.DataFrame(data) 
  
# Print the output. 
display (df) 
display (df1)


# #### 3: Creates an indexed DataFrame using arrays.

# In[5]:


# initialise data of lists. 
data = {'Gold':[46,27,26], 'Silver':[37,23,18], 'Bronze':[38,17,26]} 
  
# Creates pandas DataFrame. 
df = pd.DataFrame(data, index =['USA', 'Great Britain', 'China']) 
  
# print the data 
df


# #### 4: Creating Dataframe from list of dictionaries

# In[6]:


import pandas as pd 
  
# Intitialise data of lists  
data = [{'Silver': 3, 'Bronze':2}, {'Gold': 46, 'Silver': 37, 'Bronze': 38},  {'Gold': 27, 'Silver': 23, 'Bronze': 17}] 
  
# Creates padas DataFrame by passing  
# Lists of dictionaries and row index. 
#Please note where there is no value for any column it is marked as NaN(a value which signifies not a number and will be covered more in Numpy)
df = pd.DataFrame(data, index =('Mexico', 'USA', 'Great Britain')) 
  
# Print the data 
df 


# #### 5: Creating DataFrame using zip() function.

# In[8]:


# List1  
Team = ['Reg', 'Liq', 'Accounting', 'BIMI']  
    
# List2  
INC_COUNT = [25, 30, 26, 22]  
    
# get the list of tuples from two lists.  
# and merge them by using zip().  
list_of_tuples = list(zip(Team, INC_COUNT))  
    
# Assign data to tuples.  
# list_of_tuples   
  
  
# Convert lists of tuples into  pandas Dataframe.  

df = pd.DataFrame(list_of_tuples, columns = ['Team', 'INC_COUNT'], index=['A','B','C','D'])  
     
# Print data.  
df  


# #### 6: Creating Dataframe from data retrieved from a table in a data base

# In[7]:


let_me_in = CO.connect(TC.UOLN_CONSTR) #Make a connection object CO is alias for CX_Oracle package here, TC is the alias for the file, imported where you have stored the DB credentials in the format below
#In the file nameed Test_Credentials.py the DB credentials are stored in the format below
# UOLN_CONSTR = '''USER NAME/PassWord@DataBaseName'''
#The query you want to fire in the DB - A sample query given here
query = '''
SELECT TRAD_APPLICATION_INSTALLATION,TRAD_ROOT_CONTRACT_ID,TO_CHAR(TRAD_MATURITY_DATE, 'DD-MON-YYYY') as TRAD_MATURITY_DATE
FROM LPS_DATA.LIQ_DATA_EXTRACT 
WHERE 1                          =1
AND AS_AT_DATE                   = '28-FEB-2020'
AND ROWNUM < 10
'''

#The first parameter passed here is the SQL statement (stored in the variable  'query' and the second parameter the connection object made to connect to DB)

df = pd.read_sql(query,con=let_me_in) 
df


# #### 7: Creating Dataframe from an existing CSV/ EXCEL File

# In[8]:


df = pd.read_excel('Issues_Details.xlsx') # Withing single quotes put the excel / CSV file you want to import
df


# In[ ]:




