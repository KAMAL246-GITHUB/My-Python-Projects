#!/usr/bin/env python
# coding: utf-8

# ## Lambda Expression (Anonymous function)

# #### Introduction

# In[ ]:


lst = [2,5,8,9]
# def multi(elem):
#     '''
#     This fucntion is going perform some mathematical operations.
#     '''
#     return elem*3/2


# Alternative way:

for i in lst:
    lst2.append((lambda x: x*3/2)(i))
lst2
    


# #### With multiple arguments

# In[ ]:


func = lambda i, j : i * j+3
print(func(5, 6))


# #### Function within fucntion

# In[ ]:


def myfunc(num):
  return lambda a : a * num
myfunc(3)


# ## Filter

# In[ ]:


# Program to filter out only the even items from a list
def func(x):
    return (x%2 == 0)
    

my_list = [1, 5, 4, 6, 8, 11, 3, 12]


new_list = list(filter (func, my_list))

print(new_list)


# In[ ]:


# Program to filter out only the even items from a list
my_list = [1, 5, 4, 6, 8, 11, 3, 12]

new_list = list(filter(lambda x: (x%2 == 0) , my_list))

print(new_list)


# ## Map

# In[ ]:


# Program to double each item in a list using map()
my_list = [1, 5, 4, 6, 8, 11, 3, 12]


new_list = list(map(lambda x: x * 2 , my_list))

Output: [2, 10, 8, 12, 16, 22, 6, 24]
print(new_list)


# ## List comprehension (Advanced Usage)

# #### With  for loop

# In[ ]:


# Initialize `new_list`
new_list = []
numbers = range(10)
# Add values to `new_list`
for n in numbers:
    if n%2==0:
        new_list.append(n**2)
# Print `new_list`
print(new_list)


# #### With List comprehension

# In[ ]:


# numbers = range(10)

# # Create `new_list` 
# new_list = [n**2 for n in numbers if n%2==0]

# # Print `new_list`
# print(new_list)

[n**2 for n in range(10) if n%2==0]


# #### List Comprehension with condtionals

# In[ ]:


num = range(20)
new_list1 = [x/2 for x in num if x%2==0]
new_list2 = [x+5 for x in num if x%2!=0]
print (new_list1, new_list2)


# In[ ]:


num = range(100)
new_list = [x for x in num if x%2==0 if x%3==0]
new_list


# In[ ]:


num = range(10)
new_list = [x if x%2==0 else x*2 for x in num]
new_list


# In[ ]:


lol = [[1,2,3],[4,5,6],[7,8]]
# Flatten lol
[y  for x in lol for y in x ]


# ## Assignement

# #### list1 is the input list. Write a line of code using list comprehension with nested loops to create list which would contain twice each element of list1's inner lists.

# In[ ]:


list1 = [[1,2,3],[4,5,6],[7,8]] #input list 
[[y*2 for y in x] for x in list1]
# list2 = [[2,4,6],[8,10,12], [14,16]] #Desired output list


# In[ ]:




