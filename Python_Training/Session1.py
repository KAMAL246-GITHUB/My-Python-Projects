#!/usr/bin/env python
# coding: utf-8

# In[41]:


### See your python/ Anaconda version 

import sys 
print(sys. version)
from platform import python_version
print(python_version())

### Start With "Hello World"

print ('Hello World')
print (4)
a = 3.5
print (type(a))
print (a)

### Constants, Variables, Assignment &  Expressions

# print (1)
# print (3.8)
# print ('This is a string')

#Assignment
a = 7
b = 3.5
print (a)
print (b)
print (f"{a},{b}") #fstring
a,b = b,a
print (a)
print (b)


# In[13]:


#list of reserved keywords
import keyword
print (keyword.kwlist


# In[23]:


#Operation is performed with same types of data types
# d = "Hello" + " There"
# d = "Hello" +' '+ 1
# print (d)
# print (float('50')+1) #implicit coversion
# print ('100'+'1')
# print (100+1)


# In[43]:


#Operator precedence
#PPMAL - for Power associativity is right to Left and for rest it is left to right
# P - PArenthesis
# P - Power / Exponent
# M - Multiplication / Division 
# A - Addition / Subtraction 
# L - Logical Operator

#     ->->->->->->->->
x = 100+40*50/200-4**2
print (x)
#   <-<-<-<- start calculating the power from this side
x = 2**3**2
print (x)

x = (2**3)**2 #Parentheis takes priority
print (x)


print ('v'*3)


# ### Input function

# In[30]:


Name = input('Enter your name: ')
# print ("Oh Hello - ", Name)
# print (type(Name))


# ### Program to claculate Celsius from Farenhit

# In[31]:


faren = input('Enter the temperature in Farenhit: ')
# print (type(faren))
cel = (float(faren) - 32) * (5/9)
print ("The temperature converted to Celsius is: ", cel)


# In[1]:


import this


# In[ ]:




