#!/usr/bin/env python
# coding: utf-8

# In[29]:


import pandas as pd
import numpy as np
pd.set_option('display.max_colwidth', None)


# ### Work on Index

# In[30]:


df_actor = pd.read_csv('actors.csv')
df_new = df_actor[(df_actor['duration'] <= 100)
            & (df_actor['rating'] > 7.5)]
# df_new


# In[32]:


df_new.reset_index(drop = True, inplace = True)


# In[ ]:


df_new.set_index('name', inplace = True)


# In[ ]:


df_new.index.name


# In[ ]:


df_new.rename_axis('Movie_Name', inplace = True)


# In[ ]:


df_new = df_new.sort_index()


# In[ ]:


df_new#.reset_index()


# In[ ]:


df_new.index = df_new.index.str.strip()
# df_new.loc[['Lilies of the Field']]
# df_new.loc['Lilies of the Field':'Separate Tables', ['year','synopsis']]
df_new


# In[ ]:


df_new.reset_index().set_index(['Movie_Name','year'])


# ### Dealing with NaN Values

# #### DROPNA & ISNULL

# In[ ]:


# Select all the rows / column with NaN Values
#df_new[df_new.isna().any(axis=1)]
df_new[df_new.isnull().any(axis=1)] #python 3.6 above #Why axis=0 will not work?


# In[ ]:


# df_new['metacritic'].isnull()
# df_new[df_new['metacritic'].isnull()]
# df_new[~df_new['metacritic'].isnull()]


# In[ ]:


pd.options.mode.chained_assignment = None
df_new.loc[7] = np.NaN
df_new['Sample_Col'] = np.NaN


# In[ ]:


# df_new.dropna()
# df_new.dropna(how = 'all', axis = 1)
df_new.dropna(thresh = 10) #Keep only columns with at least two no - NA values


# #### FILLNA

# In[44]:


df_new

# df_new.fillna("****Not Available***") #Fill with specific value
# df_new.fillna(1111111) #Fill with specific value


# df_new.fillna(method='ffill') # Forward Fill 
# df_new.ffill() # Same as above

# df_new.fillna(method='bfill') # Backward Fill
# df_new.bfill() # Same as above

#Only replace the first Nan Value
# df.fillna(value=values, limit=1)


dic = {'genre2':'No Genre','metacritic': 'No Rating'}
df_new.fillna(value = dic) # Fille the nan values of different columns with different values as provided in the dictionary abvoe


# In[ ]:





# In[ ]:




