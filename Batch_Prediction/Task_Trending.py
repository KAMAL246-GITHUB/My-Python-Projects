import cx_Oracle
import numpy as np
import Credential
import pandas as pd
from  matplotlib import pyplot as plt
import copy
import ETA_SQL as ES # ETA_SQL.py file contains all the oracle SQLs used to fetch data from DB
import datetime as dt
import pytz

from IPython.display import display, HTML # Used in Jupyter
pd.set_option("display.max_rows", 1000) # To set values of the number of rows which can be displayed without truncation of rows
pd.set_option("display.max_colwidth", None) # To set values of the column width which can be displayed without truncation

# The class below stores color codes in varibales to be used later for display. Particularly useful in Jupyter. May not work on all the platforms in similar way
#Sample usage : print(color.BOLD + color.RED + color.UNDERLINE  +'Hello ALL !' + color.END)

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

##########################################################################################################
############################################## get_LRIstream_runtime #####################################
##########################################################################################################

def get_LRIstream_runtime(js):
    '''
    This function takes the job stream name as input, connects to DB, fetches the runtime and plots  a chart where last 5 days' 
    average run time is plotted along side latest COB's run time.
    It also prints the dataframe with duration details and stylesheet applied on it.
    It prints the time taken or the ETA for the jobs streams as well.
    '''
    connstr=Credential.POLN_CONSTR
    conn = cx_Oracle.connect(connstr)
    df3 = pd.read_sql(ES.LRI_ETA_Query3,con=conn, params= {'stream':js})

    df3['SESS_NAME'] = df3['SESS_NAME'].astype('str')
    df3['COB'] = df3['SES_BEG'].str.replace(' \d{2}:\d{2}:\d{2}', '', regex=True)
    df3['SES_BEG'] = pd.to_datetime(df3['SES_BEG'])
    df3['SES_END'] = pd.to_datetime(df3['SES_END'])


    def latest_rundate():
        '''
        This function returns the latest rundate of the batch based on the current day (based on the COB logic/ concept).
        '''
        latest_date = dt.datetime.now(tz=pytz.timezone('Europe/London'))
        if latest_date.strftime('%A') == 'Monday':
            return (latest_date - dt.timedelta(days=2)).strftime('%Y-%m-%d')
        elif latest_date.strftime('%A') == 'Sunday': 
            return (latest_date - dt.timedelta(days=1)).strftime('%Y-%m-%d')
        else:
            return latest_date.strftime('%Y-%m-%d')

    def apply_rownum_decorator(func):
        '''
        Decorator function to store the current row and previous row of a dataframe.This enables other function (the one passed as an 
        input to this function) to work on the values of previous or current row to derive a new column.
        It returns a wrapper function which contains the desired value.
        '''
        prev_row = {}    # For the first iteration declare the previous row as a blank dictionary
        def wrapper(cur_row, **kwargs):
            '''
            This inner/ wrapper function takes two arguments: Current row of the dataframe upon whose 'apply' was called upon
            and **kwargs holds the values for previous row passed in the form of a dictionary.
            '''
            val = func(cur_row, prev_row) # Call the function which triggered this decorator to get the calculated value for the new column 
            prev_row.update(cur_row) # Update the prev row dictionary witht he values of current row. 
            prev_row['ROW_NUM_OLD'] = cur_row['ROW_NUM'] # Preserve the current row's ROW_NUM column value in a key named ROW_NUM_OLD
            prev_row['ROW_NUM'] = val # Update the ROW_NUM of prev row with val fetched from the func
            return val # This is the value which apply function will get to make the new column.
        return wrapper

    @apply_rownum_decorator
    def find_newrownum(cur_row, prev_row):
        if prev_row == {}:
            return cur_row['ROW_NUM']
        elif (str(prev_row['SESS_NAME'])+ str(prev_row['SB_NO']) == str(cur_row['SESS_NAME']) + str(cur_row['SB_NO']) ):
            return prev_row['ROW_NUM']
        else:
            return cur_row['ROW_NUM']

    @apply_rownum_decorator
    def find_finalrownum(cur_row, prev_row):
        if (prev_row == {} or cur_row['COB'] != prev_row['COB']):
            return cur_row['ROW_NUM']
        elif (cur_row['ROW_NUM'] == prev_row['ROW_NUM_OLD'] ):
            return prev_row['ROW_NUM']
        else:
            return prev_row['ROW_NUM'] + 1

    def df_past_modify(df_past_raw):
        '''
        This function will take the raw past COB data as input and remove the rows for duplicate 
        runs on any day. It will keep only one set of stream execution 
        '''
        vcounts = df_past_raw['COB'].value_counts()
        if vcounts.value_counts().count() > 1:
            more = vcounts.value_counts().idxmax()
            less_lst = vcounts[vcounts != more].index.tolist()
            df_past_copy = df_past_raw.copy()
            df_past_copy.sort_values('SES_BEG', ascending=False, inplace = True)
            concat_list = [df_past_copy[df_past_copy['COB'] == less_lst[i]].iloc[:more , :] for i in range(len(less_lst))]
            concat_list.insert(0,df_past_copy)
            return pd.concat(concat_list).drop_duplicates(keep=False).sort_values('SES_BEG')
        else:
            return df_past_raw


    df3['ROWNUM_NEW'] = df3.apply(find_newrownum, axis =1  )
    df3.drop(columns = 'ROW_NUM', inplace = True)
    df3.rename(columns = {'ROWNUM_NEW': 'ROW_NUM'}, inplace = True)

    df3['ROWNUM_NEW'] = df3.apply(find_finalrownum, axis =1  )
    df3 = df3.reindex(columns=(['ROW_NUM','ROWNUM_NEW'] + [a for a in df3.columns if (a != 'ROWNUM_NEW' and a != 'ROW_NUM')] ))
    df3.drop(columns = 'ROW_NUM', inplace = True)


    today_dt = latest_rundate()
    filt= df3['SES_BEG'].astype('str').str.startswith(today_dt)
    df_today = df3[filt]
    df_past_raw = df3[~ filt]
    df_past = df_past_modify(df_past_raw)
    df_today_grp = df_today.groupby(['ROWNUM_NEW','SESS_NAME'])[['DURATION_IN_MIN']].max().reset_index()
    df_past_grp = df_past.groupby(['COB','ROWNUM_NEW','SESS_NAME'])[['DURATION_IN_MIN']].max().reset_index()
    df_past_aggr = df_past_grp.groupby(['ROWNUM_NEW','SESS_NAME'])[['DURATION_IN_MIN']].mean().reset_index()
    df_final =  df_today_grp[['ROWNUM_NEW','SESS_NAME','DURATION_IN_MIN']].merge(
        df_past_aggr[['ROWNUM_NEW','SESS_NAME','DURATION_IN_MIN']], 
        how = 'right',
        on = ['ROWNUM_NEW','SESS_NAME']
        )\
        .rename(columns = {'DURATION_IN_MIN_x': 'DURATION_TODAY', 'DURATION_IN_MIN_y': 'AVG_DURATION'})
    
    ############################# Apply Stylesheet to highlight and display the dataframe #############################

    df_display = df_final.set_index('ROWNUM_NEW').fillna('RUNNING', limit=1).fillna('YET TO START')
    def Color_It(d):
        '''
        This function returns colours for the backgrounds
        See more colours in https://htmlcolorcodes.com/
        '''
        w = len(d)
        dt = d['DURATION_TODAY']
        da = d['AVG_DURATION']

        if (dt == 'RUNNING' or dt == 'YET TO START'):
            return ['background-color:'] * w
        elif (dt > da+15):
            return ['background-color: #FE1203'] * w
        elif (dt > da+5):
            return ['background-color: #FEFA03'] * w
        elif (dt < da -5 ):
                return ['background-color: #25FE03'] * w
        else:
            return ['background-color:'] * w
    
    print(color.BOLD + color.RED + color.UNDERLINE+ f'''DETAILS FOR {js.strip('%')} STREAM'''+ color.END)
    try:
        display(df_display.style.apply(Color_It, axis=1))
    except:
        return (f'The script is not able to generate Chart / ETA for {js}. Please check this in ODI')

    #################################### Print ETA / time taken to complete ###################################

    print( color.BOLD + color.BLUE +"\n\n\n\n"+ f'''
          Now it is {pd.Timestamp.now('Europe/London').strftime('%H:%M:%S')} HRS (London Time)
          The Jobstream usually takes approximately {round(df_final['AVG_DURATION'].sum(),2)} mins. (May be 10 mins more or less.)'''+ color.END)

    T_BEG = pd.to_datetime(df_today['SES_BEG'].values[0]).tz_localize('Europe/London') #Find when the job stream started and then convert the time to London zone even though it may already be in it.
    T_END = pd.to_datetime(df_today['SES_END']).max().tz_localize('Europe/London') #Calculate the maximum time from session end column as that would be the last time and convert to London time zone
    TN = pd.Timestamp.now('Europe/London') # What is the time now? and then convert it to London time zone
    so_far = (TN-T_BEG).seconds/60
    tot_time = (T_END-T_BEG).seconds/60

    if (df_final['DURATION_TODAY'].isnull().any()):
        ETA = pd.to_datetime(
            df_today[df_today['ROWNUM_NEW'] == df_final[~df_final['DURATION_TODAY'].isnull()]['ROWNUM_NEW'].values[-1]]\
            ['SES_END']).max()\
            +  pd.Timedelta(minutes  = round(df_final[df_final['DURATION_TODAY'].isnull()]['AVG_DURATION'].sum(), 2) + 10 )
        print(color.BOLD + color.RED + f'''          Today it has taken {round(so_far,2)} mins so far.
          It may complete by approximately {ETA} HRS London Time.'''+ color.END)
    else:
        print (color.BOLD + color.BLUE + f'''          Today it took {round(tot_time,2)} mins to complete.''' + color.END)

    #################################### Poltting the Data ###################################

    fig,ax = plt.subplots(figsize=(20,7))
    x = np.arange(len(df_final))
    y1 = df_final['DURATION_TODAY']
    y2 = df_final['AVG_DURATION']
    plt.plot(x, y2, color = 'dodgerblue', label = 'AVG RUNTIME', marker = "s")#,linewidth = 3
    plt.plot(x, y1, color = 'red', label = 'CURRENT RUNTIME' , marker = "o")
    ax.fill_between(x,y1,y2,facecolor = 'grey', alpha = 0.4)

    #Beautify the chart
    plt.xlabel("\n TASK RUNORDERS", color = 'grey', fontsize = 16)
    plt.ylabel("\n TIME TAKEN (in mins) \n", color = 'grey', fontsize = 16)
    plt.style.use('bmh')
    plt.tick_params(left = False, bottom = False, labelsize = 14, color = 'grey')
    plt.box(False)
    legends = plt.legend(frameon = False, fontsize = 13)
    plt.setp(legends.get_texts(), color = 'darkgrey')
    plt.xticks(rotation = '75')
    plt.title("\n"+"Runtime Prediction for: "+js.strip('%')+"\n\n", fontsize = 16, color = 'grey')
    plt.xticks(x)
    ax.set_xticklabels(x+1)
    plt.show();

    
##########################################################################################################
############################################## get_FDMstream_runtime #####################################
##########################################################################################################
    
def get_FDMstream_runtime(js):
    '''
    This function takes the job stream name as input, connects to DB, fetches the runtime and plots  a chart where last few days' 
    average run time is plotted along side latest COB's run time.
    It also prints the dataframe with duration details and stylesheet applied on it.
    It prints the time taken or the ETA for the jobs streams as well.
    '''
    connstr=Credential.POGB_CONSTR
    conn = cx_Oracle.connect(connstr)
    df1 = pd.read_sql(ES.FDM_ETA_Query,con=conn, params= {'stream':js})

    df_chart = copy.deepcopy(df1)
    df_chart['DURATION'] = df_chart['DURATION'].astype('float')
    df_chart['AVG_DURATION'] = df_chart['AVG_DURATION'].astype('float')

    ############################# Apply Stylesheet #############################

    df1 = df1.fillna('RUNNING', limit=1).fillna('YET TO START')
    def Color_It(d):
        '''
        This function returns colours for the backgrounds
        See more colours in https://htmlcolorcodes.com/
        '''
        w = len(d)
        dt = d['DURATION']
        da = d['AVG_DURATION']

        if (dt == 'RUNNING' or dt == 'YET TO START'):
            return ['background-color:'] * w
        elif (float(dt) > da+15):
            return ['background-color: #FE1203'] * w
        elif (float(dt) > da+5):
            return ['background-color: #FEFA03'] * w
        elif (float(dt) < da -5 ):
                return ['background-color: #25FE03'] * w
        else:
            return ['background-color:'] * w

    print(color.BOLD + color.RED + color.UNDERLINE+ f'''DETAILS FOR {js.strip('%')} STREAM'''+ color.END)
    try:
        display(df1.style.apply(Color_It, axis=1))
    except:
        return (f'The script is not able to generate Chart / ETA for {js}. Please check this on SGL Dashboard')

    ############################# Print ETA or Completion Time #############################
    print( color.BOLD + color.BLUE +"\n\n\n\n"+ f'''
          Now it is {pd.Timestamp.now('Europe/London').strftime('%H:%M:%S')} HRS (London Time)
          The Jobstream usually takes approximately {round(df_chart['AVG_DURATION'].sum(),2)} mins. (May be 10 mins more or less.)'''+ color.END)

    TN = pd.Timestamp.now('Europe/London') # What is the time now? and then convert it to London time zone
    T_BEG = pd.to_datetime(df_chart[~df_chart['RUN_TIME'].isnull()]['RUN_TIME']).min().tz_localize('Europe/London')
    so_far = (TN-T_BEG).seconds/60

    if (df_chart['RUN_TIME'].isnull().any()):
        T_LAST = pd.to_datetime(df_chart[~df_chart['RUN_TIME'].isnull()]['RUN_TIME']).max().tz_localize('Europe/London') # Get the last logged runtime and then localize it to Europe London Time zone
        T_FRM_LAST = TN - T_LAST
        T_DUR = pd.Timedelta(minutes  = int(df1[df1['DURATION'] == 'RUNNING']['AVG_DURATION'].values[0]))
        if T_DUR > T_FRM_LAST:
            T_REM = T_DUR - T_FRM_LAST
        else:
            T_REM = pd.Timedelta(minutes  = 0)
        ETA = pd.to_datetime(df_chart[~df_chart['RUN_TIME'].isnull()]['RUN_TIME'].values[-1])\
         +  pd.Timedelta(minutes  = round(df_chart[pd.isnull(df_chart['DURATION'])]['AVG_DURATION'].sum(), 2))\
         + T_FRM_LAST + T_REM
        print(color.BOLD + color.RED + f'''          Today it has taken {round(so_far,2)}  mins so far(for the completed tasks).
          It may complete by {ETA} HRS GMT.'''+ color.END)
    else:
        print (color.BOLD + color.BLUE + f'''          Today it took {round(df_chart['DURATION'].astype('float').sum(), 2)} mins to complete.''' + color.END)

    ############################# Start Plotting #############################

    fig,ax = plt.subplots(figsize=(20,7))
    ax.clear()
    x = df_chart['TASK_RUN_ORDER']
    y1 = df_chart['DURATION']
    y2 = df_chart['AVG_DURATION']
    plt.plot(x, y2, color = 'dodgerblue', label = 'AVG RUNTIME: 1 MONTH DATA', marker = "s")#,linewidth = 3
    plt.plot(x, y1, color = 'red', label = 'CURRENT RUNTIME' , marker = "o")
    ax.fill_between(x,y1,y2,facecolor = 'grey', alpha = 0.4)

    #Beautify the chart
    plt.xlabel("\n TASK RUNORDERS", color = 'grey', fontsize = 16)
    plt.ylabel("\n TIME TAKEN (in mins) \n", color = 'grey', fontsize = 16)
    plt.style.use('bmh')
    plt.tick_params(left = False, bottom = False, labelsize = 14, color = 'grey')
    plt.box(False)
    legends = plt.legend(frameon = False, fontsize = 13)
    # plt.setp(ax.get_xticklabels(), color = 'lightblue')
    # plt.setp(ax.get_yticklabels(), color = 'lightblue')
    plt.setp(legends.get_texts(), color = 'darkgrey')
    plt.xticks(rotation = '75')
    plt.title("\n"+"Runtime Prediction for: "+js+"\n\n", fontsize = 16, color = 'grey')
    plt.show();
