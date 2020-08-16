#!/usr/bin/env python
# coding: utf-8

# In[160]:


import pandas as pd
import numpy as np
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', 100)


# In[161]:


df = pd.read_csv('actors.csv')
# df


# ### Rename Columns  / Replace function

# #### Study more on .str.replace here : https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.str.replace.html

# In[162]:


df.columns = [col.title() for col in df.columns] #Rename all the column names in dataframe - to captilize the first letter.
# df.columns.str.replace(".$", "111", regex = True) #Use Regex to replace the last letter of all the column names with a string
# df


# In[134]:


df.rename(columns ={'Name':'Movie Name', 'Rating':'IMDB Rating'}, inplace = True) # Rename selective columns
# df


# In[163]:


df.loc[0,'Movie Name'] = 'My Fav - The Theory of Everything' # Change the Movie name text in 0th row
df.loc[0,['Movie Name','Synopsis']] = ['My Favorite - The Theory of Everything', 'Stephen Hawking Story'] # Change multiple column values  in 0th row
# df


# In[164]:


df['Synopsis'] = df['Synopsis'].str.title() # Change the whole column data
df['Metacritic'] = df['Metacritic'].astype('str') #Change the data type for the whole column 
# df


# In[157]:


# Change multiple values in a particular column - add "inplace = True" argument if you want to make the change in the dataframe.
df.replace({'Genre1':{'Comedy':'*** Comedy ***',
                     'Drama':'>>>> Drama <<<<'}
           })

## Change multiple values in a particular column  - add "inplace = True" argument if you want to make the change in the dataframe.
df.replace(to_replace = ['January', 'November'], value = 'Just a Month', regex = True)


# ### Apply Function

# #### Use dataseries apply function to make changes to all the elements of the data series - or a specific column of a dataframe. Read more at https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.apply.html

# In[156]:


#Syntax df['column name'].apply(Function name defined in separate block of code OR Lambda function)
#In the line below the Metacritic column changed: The values are first converted to string, then the lagging .0 is stripped off and then '/100 'is appended
df['Metacritic'] = df['Metacritic'].apply(lambda x:str(x).strip(".0")+" / 100")
# df


# In[ ]:




