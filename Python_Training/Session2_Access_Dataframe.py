#!/usr/bin/env python
# coding: utf-8

# ### Import Pandas & Numpy, Set the options for viewing

# In[2]:


import pandas as pd
import numpy as np
# Change the setting to show the maximum n columns 
pd.set_option('display.max_columns',15)

# Change the setting to show the maximum n rows without trimming/truncating 
pd.set_option('display.max_rows',100)

# Change the setting to show all the columns' values without trimming / truncating
pd.set_option('display.max_colwidth', None)


# ### Import a sample data file(.csv format in this case) and store in a data frame

# In[ ]:


df_actress = pd.read_csv('actresses.csv')
# df_actress


# ### What is shape of this dataframe ? How many rows and columns does this table have?
# 

# In[ ]:


# df_actress.shape
# df_actress.shape[0] #Length/ Rows
# df_actress.shape[1] #Columns


# ### Column Names, Sample Rows, First Few rows, Specific Columns

# In[ ]:



# What are the column names in this data frame?
# df_actress.columns.tolist()

# Show  the first 10 rows
# df_actress.head(20)

# Show  some random rows
# df_actress.sample(20)

# Show  specific columns: Lets talk about data series and data frame difference on this context
# df_actress[['name']]
# df_actress['name']

df_actress[['name', 'duration']]


# ### Access specific rows/ columns : iloc and loc methods

# In[ ]:


# - Data for 40th row and synopsis
# df_actress.loc[<about rows>,<about the columns>]
# df_actress.loc[40,'synopsis']


# - Data for 40th till 45th row and columns - Movie name & synopsis
# df_actress.loc[40:45,['name', 'synopsis']]


# - Data for 40th till 45th row and columns - 3 till 7
# df_actress.iloc[40:45, 3:7]

# - Data for 9 & 15 th row and columns - 0,3 & 7
# df_actress.iloc[[9,15], [0,3,7]]


# - Data for till 15 th row and columns - 1 & 3
# df_actress.loc[[9,15], ['name', 'genre1', 'synopsis']]




# ###  Boolean Masking &  .str module
# 

# In[ ]:


# Show all the movies with rating 8.0

# filt = df_actress['rating']>=8.0
# df_actress[df_actress['rating']>=8.0]['name'].tolist()

# - Year for "Blue Jasmine"
# df_actress[df_actress['name'].str.strip() == 'Blue Jasmine']

# Showthe name of the movies with the most duration
# df_actress[df_actress['duration'] == df_actress['duration'].max()]
# df_actress[df_actress['duration'] == df_actress['duration'].min()]
# df_actress[df_actress['nominations'] == df_actress['nominations'].max()]

# df_actress[df_actress['duration']==df_actress['duration'].min()]

# Show all romantic movies.
# df_actress[((df_actress['genre1'].str.strip()) == 'Romance') | (df_actress['genre2'].str.strip() == 'Romance') ][['name','synopsis']]

# Show all Drama & Romantic movies.
# df_actress[(df_actress['genre1'].str.strip() == 'Drama') & (df_actress['genre2'].str.strip() == 'Romance') ]


# Show all the movies whose metacritic rating is more than 85
# df_actress[df_actress['metacritic'] > 85]

# Show all the movies whose synopsis contains the word mother
# df_actress[df_actress['synopsis'].str.contains('mother')]

# Show all the movies whose genre is not crime
filt = (df_actress['genre1'].str.contains('Crime')) | (df_actress['genre2'].str.contains('Crime'))
df_actress[~filt ]


# ### Assignement 

# There are four data sets in CSV format. They contains the movie details which won Academy awards for best actors, actresses, directors and pictures respectively.
# 
# 1)	Import the csv files to 4 different  data frames.
# 
# 2)	Make new data frames which would contain the movies with genre ‘Romance’ and have IMDB rating above 7.5  and duration below 100 mins (It will result in 4 data frames derived from the original data frames)
# 
# 3)	Now append all these 4 data frames to a single data frame. (google about Pandas append function – we have not discussed it in the session)
# 
# 4)	Once you have the final data frame ready – use unique function on the name column to get a non-repeated list of movies. (Google about Pandas unique function – we have not discussed it in the session)

# #### Import csv files in to 4 different data frames

# In[43]:


df_actress = pd.read_csv('actresses.csv')
df_actor = pd.read_csv('actors.csv')
df_director = pd.read_csv('directors.csv')
df_picture = pd.read_csv('pictures.csv')


# #### Use desired filters and make 4 new data frames

# In[44]:


df_actress_rom = df_actress[(
            (df_actress['genre1'].str.strip() == 'Romance') 
            | (df_actress['genre2'].str.strip() == 'Romance')
            ) 
            & (df_actress['duration'] <= 100)
            & (df_actress['rating'] > 7.5)]

df_actor_rom = df_actor[(
            (df_actor['genre1'].str.strip() == 'Romance') 
            | (df_actor['genre2'].str.strip() == 'Romance')
            ) 
            & (df_actor['duration'] <= 100)
            & (df_actor['rating'] > 7.5)]

df_director_rom = df_director[(
            (df_director['genre1'].str.strip() == 'Romance') 
            | (df_director['genre2'].str.strip() == 'Romance')
            ) 
            & (df_director['duration'] <= 100)
            & (df_director['rating'] > 7.5)]

df_picture_rom = df_picture[(
            (df_picture['genre1'].str.strip() == 'Romance') 
            | (df_picture['genre2'].str.strip() == 'Romance')
            ) 
            & (df_picture['duration'] <= 100)
            & (df_picture['rating'] > 7.5)]  
    


# #### Use append function to make one dataframe 

# In[47]:


df_final = df_actress_rom.copy()
df_final = df_final.append([df_actor_rom,df_director_rom,df_picture_rom],  ignore_index=True)
# df_final = df_final.drop_duplicates(keep=False).reset_index(drop=True)
df_final #['nominations'].tolist()
# ['5', '3', '7', '8', 5, 8, 6, '5', '8']
df_final['nominations'] = df_final['nominations'].astype('int64')
df_final.drop_duplicates(keep='first')
# df_final['nominations']


# #### Use Concat function to make one dataframe 

# In[61]:


df_final_con = pd.concat([ df_actress_rom, df_actor_rom, df_director_rom, df_picture_rom], ignore_index=True)
df_final_con = df_final_con.                drop_duplicates(keep=False).                reset_index(drop=True)
df_final_con


# ### DROP_DULICATES Examples

# In[84]:


# df.drop_duplicates(keep= False)
df = df[df['name'].str.contains('Annie Hall')].reset_index(drop=True)


# In[85]:


df['nominations'] = df['nominations'].astype('int64')


# In[86]:


df


# In[87]:


df.drop_duplicates(keep= 'first')


# In[71]:


print (df.loc[0].tolist())
print (df.loc[1].tolist(),)


# #### Example 2

# In[3]:


df = pd.DataFrame({'Student_Name': ['Hari', 'Rama', 'Mike','Hari','Lata', 'Jenny', 'Hari'],
                   'Subject': ['History', 'Geography', 'Physics','History','Mathematics', 'Economics', 'History'],
                  'Score':[70,72,85,70,80,83,70]})
df


# In[37]:


df.drop_duplicates(keep = False)


# In[21]:


df['Score'] = df['Score'].astype('float')


# In[22]:


df


# In[23]:


df['Score']


# In[ ]:




