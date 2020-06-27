import IN_OUT_SQL as IS
import cx_Oracle as co
import numpy as np
import Credential as cd
import pandas as pd
from  matplotlib import pyplot as plt
from matplotlib import dates as mdates
import matplotlib.ticker as tick
from IPython.display import display, HTML
import copy
%matplotlib inline
pd.set_option('display.max_columns', 30)

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'
#print(color.BOLD + color.RED + color.UNDERLINE  +'Hello ALL !' + color.END)

########################################################################################
############   Plot Bar chart with 2 or 3 bars on each group based on the SLA ##########
########################################################################################
def get_sql(MH):
    switch = {
        '1': IS.OUT_SQL_CMONTH,
        '2': IS.OUT_SQL_LMONTH,
        '3': IS.OUT_SQL_L2LMONTH
    }
    return switch.get(MH, IS.OUT_SQL_LMONTH)

def extract_data():
    conn = co.connect(cd.POLN_CONSTR)
    MH = input(f'''Which Month you want to see the trending for:
1. Current Month
2. Last Month
3. Last to Last Month
''')
    query = get_sql(MH)
    frame = pd.read_sql(query, con = conn)
    return frame

df = extract_data()
df['WSGLDN'] = df['WSGLDN'].fillna(0) # Bcause WSGLDN started from 12 APR so for the rest of the days to have this in april graph made the values 0

df.dropna(inplace=True)

# df.drop(columns = 'FXNLDN', inplace = True)
df.iloc[:,1:] = df.iloc[:,1:].apply(lambda x : pd.to_datetime(x).dt.strftime('%H%M').astype('int'))
Month = '-'.join(df['COB'][0].split('-')[1:]).upper()

df9 = df.loc[:,['COB','FXNLDN']]
df7 = df.loc[:,['COB','GDSLDN', 'GDSMNH','LQSLDN','CALV14']]
df5 = df.loc[:,['COB', 'ANVLDN', 'CALASP', 'CALLDN', 'CALMNH',
                'WSGLDN','WSRLDN', 'WSRASP', 'WSNLDN', 'WSUROI', 'WSUFAC', 'WSUNIR','WSRMNH',
                'ICELDN', 'GFXSNG', 'SYXLDN', 'ECOLDN', 'GFXMNH','GFXLDN', 'TMSLDN']]
df9['MAX'] = df9.iloc[:,1:].max(axis=1)
df7['MAX'] = df7.iloc[:,1:].max(axis=1)
df5['MAX'] = df5.iloc[:,1:].max(axis=1)

df_SLA = df7['MAX'].to_frame().merge(df5['MAX'].to_frame(), left_index=True, right_index=True)
df_SLA['MISS'] = df_SLA.apply(lambda row : 'YES' if (row['MAX_x'] > 700 or  row['MAX_y'] > 500 ) else 'NO', axis = 1)


####  Plot the graph  ####

ind  = np.arange(len(df)) #positions of bars on x axis
width = 0.4 #Width of bars

fig,ax = plt.subplots(figsize=(15,8))
ax.clear()

# bars9 = plt.bar(ind,df9['MAX'],width/2,color = 'forestgreen')
# [bar.set_color('red') for bar in bars9 if int(bar.get_height()) > 900]
# [bar.set_edgecolor( 'grey') for bar in bars9]

bars7 = plt.bar(ind+width/2,df7['MAX'],width/2,color = 'forestgreen')
[bar.set_color('red') for bar in bars7 if int(bar.get_height()) > 700]
[bar.set_edgecolor( 'grey') for bar in bars7]

bars5 = plt.bar(ind+width, df5['MAX'],width/2, color = 'forestgreen')
[bar.set_color('red')for bar in bars5 if int(bar.get_height()) > 500]
[bar.set_edgecolor( 'grey') for bar in bars5]

# plt.axhline(y = 900, color = 'dodgerblue', linestyle = '--', linewidth = 0.75)
plt.axhline(y = 700, color = 'maroon', linestyle = '--', linewidth = 0.75)
plt.axhline(y = 500, color = 'black', linestyle = '--', linewidth = 0.75)
# ax.text(bars5[-1].get_x()+1.5, 890, "09 AM SLA", color = 'darkred', fontweight='bold')
ax.text(bars5[-1].get_x()+1.5, 690, "07 AM SLA", color = 'darkred', fontweight='bold')
ax.text(bars5[-1].get_x()+1.5, 490, "05 AM SLA", color = 'darkred', fontweight='bold')
# ax.annotate("Each set of bars:\nFirst Bar :    Streams with 07 AM SLA\nSecond Bar : Streams with 05 AM SLA",
#             [ind[-1]+1.4, df7['MAX'].max()], ha='left', size=12, color = 'Black' )

# plt.legend()
ax.set_xticks(ind + width/3)
ax.set_xticklabels(df7['COB'].tolist())

plt.rcParams['axes.edgecolor'] = 'black'
plt.xticks(rotation = 75)
plt.style.use('bmh')
# plt.box(False)
plt.tick_params(bottom = False, left = False)
# ax.grid(axis = 'y', alpha =0.1)
plt.xlabel('\nCOB Dates')
plt.ylabel('Time of Delivery in 2400 HRS Format (GMT/BST as applicable)')
plt.title(f''' LRI readiness time against COBs for {Month}
        In each set : First Bar : Streams with 09 AM SLA
        Second Bar  : Streams with 07 AM SLA
        Third Bar   : Streams with 05 AM SLA
      
            ''')
#print(color.BOLD + color.RED + color.UNDERLINE  +'Hello ALL !' + color.END)

print (color.BOLD  + f'''            
            Out of {len(df_SLA)} COBs in {Month}: 
            Data was delivered on time for {len(df_SLA[df_SLA['MISS'] == 'NO'])} days.
            SLA was breached for  {len(df_SLA[df_SLA['MISS'] == 'YES'])} days.
        '''+  color.END)
plt.show();


########################################################################################
############   Same as above but with dark background                         ##########
########################################################################################


ind  = np.arange(len(df)) #positions of bars on x axis
width = 0.3 #Width of bars

fig,ax = plt.subplots(figsize=(15,6))
ax.clear()
bars7 = plt.bar(ind,df7['MAX'],width,color = 'forestgreen')
[bar.set_color('red') for bar in bars7 if int(bar.get_height()) > 700]
[bar.set_edgecolor( 'grey') for bar in bars7]
bars5 = plt.bar(ind+width, df5['MAX'],width, color = 'forestgreen')
[bar.set_color('red')for bar in bars5 if int(bar.get_height()) > 500]
[bar.set_edgecolor( 'grey') for bar in bars5]
plt.axhline(y = 700, color = 'lightgrey', linestyle = '--', linewidth = 0.75)
plt.axhline(y = 500, color = 'lightgrey', linestyle = '-', linewidth = 0.75)
ax.text(bars5[-1].get_x()+1.5, 690, "07 AM SLA", color = 'white', fontweight='bold')
ax.text(bars5[-1].get_x()+1.5, 490, "05 AM SLA", color = 'white', fontweight='bold')
ax.set_xticks(ind+width/2)
ax.set_xticklabels(df7['COB'].tolist())
plt.rcParams['axes.edgecolor'] = 'black'
plt.xticks(rotation = 75)
plt.tick_params(bottom = False, left = False, labelsize=13)
# ax.grid(axis = 'y', alpha =0.1)
plt.xlabel('\nCOB Dates\n', size = 14)
plt.ylabel('Time of Delivery in 2400 HRS Format (GMT/BST as applicable)\n')
plt.title("LRI readiness time against COBs \n")
print (f'''            
            Out of {len(df_SLA)} COBs: 
            Data was delivered on time for {len(df_SLA[df_SLA['MISS'] == 'NO'])} days.
            SLA was breached for  {len(df_SLA[df_SLA['MISS'] == 'YES'])} days.
        ''')

plt.style.use("seaborn-dark")
for param in ['figure.facecolor', 'axes.facecolor', 'savefig.facecolor']:
    plt.rcParams[param] = '#212946'  # bluish dark grey
for param in ['text.color', 'axes.labelcolor', 'xtick.color', 'ytick.color']:
    plt.rcParams[param] = '0.9'  # very light grey
ax.grid(color='#2A3459')  # bluish dark grey, but slightly lighter than background
plt.show();


########################################################################################
############   Same as above but with line plot                               ##########
########################################################################################


fig,ax = plt.subplots(figsize=(15,6))
ax.clear()
x = np.arange(len(df7['COB']))
plt.plot(x, df7['MAX'],color = 'orange', marker = "o")
plt.plot(x, df5['MAX'],color = 'dodgerblue', marker = "s")
plt.axhline(y = 700, color = 'orange', linestyle = '--', linewidth = 0.75)
plt.axhline(y = 500, color = 'dodgerblue', linestyle = '-', linewidth = 0.75)
plt.xticks(x, rotation = 75)
ax.set_xticklabels(df7['COB'].tolist())
plt.tick_params(bottom = False, left = False, labelsize=13)
plt.xlabel('\nCOB Dates\n', size = 14)
plt.ylabel('Time of Delivery in 2400 HRS Format (GMT/BST as applicable)\n')
plt.title("LRI readiness time against COBs\n")
print (f'''            
            Out of {len(df_SLA)} COBs: 
            Data was delivered on time for {len(df_SLA[df_SLA['MISS'] == 'NO'])} days.
            SLA was breached for  {len(df_SLA[df_SLA['MISS'] == 'YES'])} days.
        ''')

plt.style.use("seaborn-dark")
for param in ['figure.facecolor', 'axes.facecolor', 'savefig.facecolor']:
    plt.rcParams[param] = '#212946'  # bluish dark grey
for param in ['text.color', 'axes.labelcolor', 'xtick.color', 'ytick.color']:
    plt.rcParams[param] = '0.9'  # very light grey
ax.grid(color= '#2A3459')  # bluish dark grey, but slightly lighter than background

plt.show();

########################################################################################
############   Today's file delivery time with barplot                        ##########
########################################################################################

import IN_OUT_SQL as IS
import cx_Oracle as co
import numpy as np
import Credential as cd
import pandas as pd
from  matplotlib import pyplot as plt
from matplotlib import dates as mdates
import matplotlib.ticker as tick
from IPython.display import display, HTML
import copy
import math
import datetime as dt
import pytz
%matplotlib inline
pd.set_option('display.max_columns', 30)

conn = co.connect(cd.POLN_CONSTR)
query = IS.OUT_SQL_Today2
df_raw = pd.read_sql(query, con = conn)
df_today = df_raw.copy(deep=True)
# flt = df_today['APPLICATION_INSTALLATION'] == 'RRSLDN'
# df_today.loc[flt, 'COMPLETION_TIME'] = np.nan
# df_today.dropna(inplace = True)
df_today.iloc[:, 1:] = df_today.iloc[:, 1:].apply(lambda x : x if x is None else pd.to_datetime(x).dt.strftime('%H%M').astype('float') )
df_today


# #######################  Plot #######################

ind = np.arange(len(df_today))
fig,ax = plt.subplots(figsize=(15,8))
ax.clear()

bars = plt.bar(ind, df_today['COMPLETION_TIME'], color = 'forestgreen')
for bar in bars[:21]:
    if bar.get_height() > 500:
        bar.set_color('red')
for bar in bars[21:25]:
    if bar.get_height() > 700:
        bar.set_color('red')
for bar in bars[25:]:
    if bar.get_height() > 900:
        bar.set_color('red')




plt.axhline(xmax = .95,y = 900, color = 'dodgerblue', linestyle = '--', linewidth = 0.75)
plt.axhline(xmax = .92, y = 700, color = 'maroon', linestyle = '--', linewidth = 0.75)
plt.axhline(xmax = .77 ,y = 500, color = 'black', linestyle = '--', linewidth = 0.75)
ax.text(-4, 890, "09 AM SLA", color = 'darkred', fontweight='bold')
ax.text(-4, 690, "07 AM SLA", color = 'darkred', fontweight='bold')
ax.text(-4, 490, "05 AM SLA", color = 'darkred', fontweight='bold')

ax.set_xticks(ind)
ax.set_xticklabels(df_today['APPLICATION_INSTALLATION'].tolist())
plt.rcParams['axes.edgecolor'] = 'black'
plt.xticks(rotation = 75)
plt.style.use('bmh')
plt.box(False)
# ax.grid(False) #axis = 'x', alpha =0.05) #Remove the grid lines by passing argument to False or make it less prominent via alpha value
plt.xlabel('\nStreams', fontsize = 15)
plt.ylabel('\n\nTime of Delivery in 2400 HRS Format (GMT/BST as applicable)', fontsize = 12)
ax.yaxis.set_label_position("right") # Shift y label to right
# ax.yaxis.tick_right() # Put the y tick labels to right
ax.tick_params(bottom = False, left = False, right = False)
plt.setp(ax.get_yticklabels(), color="lightgrey")
plt.title(f''' LRI readiness time Today
''', fontsize = 15)

def anotate_bars(bar):
    '''
    This function helps annotate the bars with data labels in the desired position.
    '''
    def say_h(x,num):
            #line 77 to 82 define the SLA variable based on which streams are passed
            if (num > 20 and num < 25):
                SLA = 700
            elif (num >= 25):
                SLA = 900
            else:
                SLA = 500
            
            #Below if else block defines what comment to be put instead of bar if the stream has not completed yet    
            if math.isnan(x):
                now = int(dt.datetime.now(tz=pytz.timezone('Europe/London')).strftime('%H%M')) # What is the time now ? strip only hours and minutes and then convert it to integer
                comment = input(f"Enter the ETA or Reason of delay for {(df_raw.loc[num,'APPLICATION_INSTALLATION'])} : ")
                
                # Make the colour of the comment red if stream has not been deliverd yet and already breached SLA else blue
                if now > SLA:
                    c = 'red'
                else:
                    c = 'blue' #'#900C3F' # "#900C3F" is the hexa color code for Maroon - ref https://htmlcolorcodes.com/
                    
                if comment.strip()=='':
                    return ('Pending', c) 
                else:
                    return (comment, c)
            else:
                return (str(df_raw.loc[num,'COMPLETION_TIME']), 'black')
    def say_y(n):
            if math.isnan(n):
                return 0
            else:
                return n
        
    for num, bar in enumerate(bars):
        h = bar.get_height() # Get Height of the bars
        text, col = say_h(h,num) # Text and colour of the text to be annotated
        x_pos = bar.get_x()+bar.get_width()/2 # Xpostion of the text
        y_pos = say_y(h)+15  # Ypostion of the text
        ax.text(x_pos,y_pos, text ,ha='center', va='bottom', color = col, rotation = 90, fontsize = 12) #, fontweight='bold')

anotate_bars(bar)
plt.show();

#Sample Comments
# ABC Delay ETA 1000 HRS BST
# ETA 1000 HRS BST 

########################################################################################
############   Today's file delivery time with scatterplot                    ##########
########################################################################################



def extract_data_today():
    conn = co.connect(cd.POLN_CONSTR)
    query = IS.OUT_SQL_Today
    frame = pd.read_sql(query, con = conn)
    return frame

df_today = extract_data_today()
# df_today.drop(columns = 'FXNLDN', inplace = True)
df_today.iloc[:,1:] = df_today.iloc[:,1:].apply(lambda x : pd.to_datetime(x).dt.strftime('%H%M').astype('int'))
#df_today = dfT[df['COB']=='28-Feb-2020']
df_today1A3A = df_today[['COB','GDSLDN', 'GDSMNH','LQSLDN','CALV14']]
df_today3b = df_today[['COB','ANVLDN', 'CALASP', 'CALLDN', 'CALMNH','WSRLDN', 'WSRASP', 'WSNLDN', 'WSUROI', 'WSUFAC', 'WSUNIR','WSRMNH','ICELDN', 'GFXSNG', 'SYXLDN', 'ECOLDN', 'GFXMNH','GFXLDN', 'TMSLDN']]
df_todayFXN = df_today[['COB','FXNLDN']]
df_today1A3A = df_today1A3A.T
df_today1A3A.drop('COB', inplace = True)
df_today3b = df_today3b.T
df_today3b.drop('COB', inplace = True)
df_todayFXN = df_today[['COB','FXNLDN']].T
df_todayFXN.drop('COB', inplace = True)

fig,ax = plt.subplots(figsize=(15,8))
ax.clear()
x1=df_today1A3A.index
y1=df_today1A3A[0]
x2=df_today3b.index
y2=df_today3b[0]
x3=df_todayFXN.index
y3=df_todayFXN[0]

col1 = np.where(y1<700,'green','r')
col2 = np.where(y2<500,'green','r')
col3 = np.where(y3<500,'green','r')
plt.scatter(x1,y1,c=col1, s =1200, alpha = 0.6)
plt.scatter(x2,y2,c=col2, s =1200, alpha = 0.6)
plt.scatter(x3,y3,c=col3, s =1200, alpha = 0.6)

for i,txt in enumerate(y1):
    ax.annotate("0"+str(txt),[i, y1[i]], ha='center', size=12, rotation = 75)
for i,txt in enumerate(y2):
    ax.annotate("0"+str(txt),[i+4, y2[i]], ha='center',size=12, rotation = 75)
for i,txt in enumerate(y3):
    ax.annotate(txt,[i+22, y3[i]], ha='center', rotation = 75)
    
plt.xticks(rotation = 75, size = 12)
plt.style.use('bmh')
# plt.box(False)
plt.tick_params(bottom = False, left = False)
plt.xlabel('\nLRI Streams',  size=16)
plt.ylabel('Time of Delivery (GMT/BST as applicable)\n', size=16)
plt.title("Today's file delivery time\n", size=16)
plt.show();

