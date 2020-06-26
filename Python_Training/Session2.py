#!/usr/bin/env python
# coding: utf-8

# ## Conditional Statements

# #### If Else

# In[ ]:


# Indentation is very important in python
# > , >=
# < , <=
# ==, =, !=


liq_inc_num = int(input("Enter the incident numbers in your area this month:"))
# Remember that input function converts the input data to string data trype 

if liq_inc_num < 30:
    print ('Liquidity Folks - excellent job!')
elif liq_inc_num < 50:
    print ('Good job - see if any other area of improvement is there.')
else:
    print ('Please follow the incident remediation process.')
    
    
## Only if or if-else block works too.


# #### Try/ Except : Error Handling

# In[ ]:


x = input('Enter a number:')

try:
    print (int(x)*10)
except:
    print('Probably the number you entered, contains a charachter. Try Again!')


# #### For Loop

# In[14]:


# for i in range(1,30):
#     print (i)

n = 30
for i in range(1, n): ## Print a staircase 0,1,2,3,4,5,6,7,8,9
    if i < 15:
            print ((n-i)*" " + "#"*i)
    else:
        print ((n-i)*" " + "*"*i)
    


# #### While Loop

# In[10]:


num = 0
acum = 0
while num < 4:
    num = num + 1 #num += 1   3
    acum = acum + num #6
print (acum)


# #### Looping with break, continue

# In[11]:


largest = 0
smallest = 0
while True:
    num = input('Enter a number:')
    if num == 'done' or num == 'Done' or num == 'DONE':
        break
    try:
        num = float(num)
    except:
        print ("Enter a valid number: ")
        continue
    if largest == 0:
        largest = num
    if smallest == 0:
        smallest = num
    if num > largest:
        largest = num
    if num < smallest:
        smallest = num
print ("Largest of the numbers is: " , str(largest))
print ("Smallest of the numbers is: " , str(smallest))        


# #### Function 

# In[5]:


def my_first_func():
    print ('Great - you just invoked your first python function!!')
my_first_func()


# In[12]:


def incident_count(tm):
    '''
    This function takes the team name as input and provides the list of application they support.
    '''
    
    if tm == 'Liquidity':
        print ("Liquidity Team supports below applications:\n\nICO \nLPS \nTableau \nCognos \nSteel")
    if tm == 'Risk':
        print ('''Risk Team supports below applications:
                GRDW
                Frank''')
        
    if tm == 'Reg':
        print ("Reg Team supports below applications:\n\nBOE \nFINREP \nVADER \nRCUBE \nEDGS \nAXIOM")

# incident_count('Risk')
help (incident_count) # To know what a function does


# In[13]:


def my_cube(num):
    return num*num*num
my_cube(3)


# #### Function with default arguments

# In[17]:



# Function definition is here
def teaminfo( Team, Manager = 'Gaurav' ):
   '''
   This prints a passed info into this function
   '''
   print ("Team: ", Team)
   print ("Manager: ", Manager)
#    return;

# Now you can call printinfo function
# teaminfo( Team='Reg', Manager="Avanish" )
# teaminfo( Team="Accounting" )

# help(teaminfo)


# In[ ]:




