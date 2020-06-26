#!/usr/bin/env python
# coding: utf-8

# ## Connect to a Database and perform DB operations using Python

# #### Import libraries / modules / path

# In[ ]:


import cx_Oracle as  CO
import sys
sys.path.insert(1, r'D:\Users\sahook\Desktop\Scripts\PYTHON3') #Includes this path in the default paths to be refered while looking for any python module
import Test_Credentials as TC


# ### Select from the data base

# In[ ]:


conn = CO.connect(TC.UOLN_CONSTR) #Make a connection object
cur = conn.cursor()#Create a cursor

cur.execute('''
SELECT TRAD_APPLICATION_INSTALLATION,TRAD_ROOT_CONTRACT_ID,TO_CHAR(TRAD_MATURITY_DATE, 'DD-MON-YYYY') as TRAD_MATURITY_DATE
FROM LPS_DATA.LIQ_DATA_EXTRACT 
WHERE 1                          =1
AND AS_AT_DATE                   = '28-FEB-2020'
AND ROWNUM < 10
'''
) #Execute a smaple insert query - result is stored in cur


row_list = [value for value in cur] # Retrieve the query output stored in 'cur' through a list comprehension and put in row_list
print (*row_list, sep="\n") #print it in a more readable way
cur.close() #Close the cursor
conn.close() #Close the Connection


# ### Create a table 

# In[ ]:


conn = CO.connect(TC.UOLN_CONSTR) #Make a connection object
cur = conn.cursor()#Create a cursor
cur.execute('''
CREATE TABLE DROP_ME_SAMPLE
( TRADE_ID number(10) NOT NULL,
  REGION_NAME varchar2(50) NOT NULL,
  TRADE_TYPE varchar2(50),
  CONSTRAINT sample_trades_pk PRIMARY KEY (TRADE_ID)
)
'''
) #Create table
cur.close() #Close the cursor
conn.close() #Close the Connection


# ### Insert Data in Table

# In[ ]:


conn = CO.connect(TC.UOLN_CONSTR) #Make a connection object
cur = conn.cursor()#Create a cursor


cur.execute('''INSERT INTO DROP_ME_SAMPLE (TRADE_ID, REGION_NAME,TRADE_TYPE) VALUES (:TRADE_ID,:REGION_NAME,:TRADE_TYPE)''',
(10, 'LDN','COLLAT')
) #Insert Data into table

conn.commit() 
cur.close() #Close the cursor
conn.close() #Close the Connection


# ### Insert More Records

# In[ ]:


conn = CO.connect(TC.UOLN_CONSTR) #Make a connection object
cur = conn.cursor()#Create a cursor
statement = 'INSERT INTO DROP_ME_SAMPLE (TRADE_ID, REGION_NAME,TRADE_TYPE) VALUES (:TRADE_ID,:REGION_NAME,:TRADE_TYPE)'
cur.execute(statement,(13, 'ASP','FX'))
cur.execute(statement,(14, 'MNH','EP'))
cur.execute(statement,(15, 'LDN','FFP'))
cur.execute(statement,(16, 'ASP','FPRN'))
conn.commit() 
cur.close() #Close the cursor
conn.close() #Close the Connection


# ### Select Data from table

# In[ ]:


conn = CO.connect(TC.UOLN_CONSTR)
cur = conn.cursor()

cur.execute('''SELECT * FROM DROP_ME_SAMPLE ''')
row_list = [value for value in cur] # Retrieve the query output stored in 'cur' through a list comprehension and put in row_list

cur.close()
conn.close()
print (*row_list, sep="\n") #print it in a more readable way



# ### Drop the table

# In[ ]:


conn = CO.connect(TC.UOLN_CONSTR) #Make a connection object
cur = conn.cursor()#Create a cursor

cur.execute('''
DROP TABLE DROP_ME_SAMPLE
'''
) #Drop table
cur.close() #Close the cursor
conn.close() #Close the Connection


# ### Retrieve Records : PANDAS way (To be discussed in details in the upcoming sessions)

# In[ ]:


import pandas as pd
let_me_in = CO.connect(TC.UOLN_CONSTR) #Make a connection object
query = '''
SELECT TRAD_APPLICATION_INSTALLATION,TRAD_ROOT_CONTRACT_ID,TO_CHAR(TRAD_MATURITY_DATE, 'DD-MON-YYYY') as TRAD_MATURITY_DATE
FROM LPS_DATA.LIQ_DATA_EXTRACT 
WHERE 1                          =1
AND AS_AT_DATE                   = '28-FEB-2020'
AND ROWNUM < 10
'''

pd.read_sql(query,con=let_me_in)


# In[ ]:




