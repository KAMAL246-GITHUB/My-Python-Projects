#!/usr/bin/env python
# coding: utf-8

# ## Lists

# #### Create a list

# In[3]:


list1 = ['Reg', 'Liquidity', 90, 1000, 'rbs'];
list2 = [1, 2, 3, 4, 5 ];
list3 = ["a",'z','Z', "b", "c", "d"]


# #### Access list elements

# In[11]:


# print (list1[-2])
# print (list1[1:4])
# list1[::-1]


# In[9]:


list2[2] = 2001;
list2


# #### Modify a list

# In[12]:


print (list1)
del list1[2];
print (list1)


# #### Find length, Concatenate, Iterate through a list

# In[19]:


# len([1, 2, 3])  #	3	Length
# [1, 2, 3] + [4, 5, 6]#	[1, 2, 3, 4, 5, 6]	Concatenation
# ['Hi!'] * 4 #	['Hi!', 'Hi!', 'Hi!', 'Hi!']#	Repetition
# 3 in [1, 2, 3]#	True	Membership
# for x in [1, 'Char', 3]: 
#     print (x) #	1 2 3	Iteration


# In[22]:


# len(list3)
# # Gives the total length of the list.

# max(list2)
# # Returns item from the list with max value.

# min(list2)
# # Returns item from the list with min value.

# list(tup)
# # Converts a tuple into list.


# In[33]:


list2[2:4]
list2[-2]


# #### Append, Extend, Insert, Pop, Remove and Reverse a list

# In[38]:


lst = [7,6,6,3,3,3,3,7,2]
lst.append(9)
lst


# In[33]:


lst.count(3)


# In[34]:


lst2 = ['a','b','c']
lst2.extend(lst)
print (lst2)


# In[53]:


# lst2.index('c')
# Returns the lowest index in list that obj appears

# lst.insert(3,'Just inserting something')
# # Inserts object obj into list at offset index

# lst.pop()
# # Removes and returns last object or obj from list

# lst.remove(6)
# # Removes element from list

# lst.reverse()
# # Reverses objects of list in place

# list2.sort()
# # Sorts objects of list
# print (lst)


# #### Strip & Split

# In[66]:


st = ':Competition between the Old and New Banks was fierce and centred on the issue:'
# st.strip(':')
var = 77
print (var)
print (st)


# In[62]:


st = '''
Competition between the Old and New Banks was fierce and centred on the issue of banknotes. The policy of the Royal Bank was to either drive the Bank of Scotland out of business, or take it over on favourable terms.
The Royal Bank built up large holdings of the Bank of Scotland's notes, which it acquired in exchange for its own notes, then suddenly presented to the Bank of Scotland for payment. To pay these notes, the Bank of Scotland was forced to call in its loans and, in March 1728, to suspend payments. The suspension relieved the immediate pressure on the Bank of Scotland at the cost of substantial damage to its reputation, and gave the Royal Bank a clear space to expand its own business—although the Royal Bank's increased note issue also made it more vulnerable to the same tactics.
Despite talk of a merger with the Bank of Scotland, the Royal Bank did not possess the wherewithal to complete the deal. By September 1728, the Bank of Scotland was able to start redeeming its notes again, with interest, and in March 1729, it resumed lending. To prevent similar attacks in the future, the Bank of Scotland put an "option clause" on its notes, giving it the right to make the notes interest-bearing while delaying payment for six months; the Royal Bank followed suit. Both banks eventually decided that the policy they had followed was mutually self-destructive and a truce was arranged, but it still took until 1751 before the two banks agreed to accept each other's notes.
'''
lst = st.split()
print (lst)


# In[18]:


st2 = "We:have:had:5:sessions:in:python:so:far"
# st2.split(":")
lst5= ['This', 'will', 'join', 'all', 'words', 'into', 'a', 'string']
':'.join(lst5)


# ### List Comprehension 

# In[4]:


lst = [1,4,5,7]
lst2 = []

# for n in lst:
#     lst2.append(n*n+1)
    
    
lst2 = [ n*n+1 for n in lst ]


print (lst2)


# In[5]:


tup = (1,3,4,5)
tup


# ### Assignement / Problem : How to count all the words given in a string and find the top 5 most recurring words ?
#     

# In[ ]:




