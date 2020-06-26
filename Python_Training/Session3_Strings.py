#!/usr/bin/env python
# coding: utf-8

# ## Strings

# #### Accessing

# In[6]:


st = 'Finance Reporting Solution'
# print(st)

#first character
# print(st[8])

# # #last character
# print( st[-2])

# # #slicing 2nd to 5th character
# print(st[1:3])

# # #slicing 6th to 2nd last character
print('st[5:-2] = ', st[5:-2])


# #### Concatenation

# In[8]:


str1 = 'Hello'
str2 ='RBS'

# using +
print('str1 + str2 = ', str1 + str2)

# using *
print('str1 * 3 =', str1 * 3)


# #### Length

# In[9]:


len(st)


# #### Test conditions

# In[10]:


## Count all the 'l's in str
st = 'Hello Delhi'
count = 0
for i in range(len(st)):
    if st[i] == 'l':
        count += 1 #count = count +1
print (count)
# len(st)

# for i in range(1,51, 5):
#     print (i)


# #### Enumerate - We will discuss it more after studying List and Tuples

# In[9]:


st = 'Liquidity'
list_enumerate = list(enumerate(st))
print('list(enumerate(st) = ', list_enumerate)


# In[11]:


st = 'Liquidity Support comes under FRS'
print (st.lower()) #Convert to lowercase
print (st.upper()) #Convert to upper case
print (st.find('Support')) #Find the string starting position
print (st.replace('Liquidity','Regulatory')) #Replace specific substring within the string

# We will discuss it more after studying List and Tuples
print (st.split()) 
print  (' '.join(['This', 'will', 'join', 'all', 'words', 'into', 'a', 'string']))


# #### How to reverse a string

# In[13]:


st = 'Liquidity Support comes under FRS'
st[::-1] # Start at the end of the string and end at position 0, move with the step -1, negative one, which means one step backwards.


# In[ ]:




