## This script takes the Trade Root Contract ID as input and checks related data in all the relevant tables.

import pandas as pd
import numpy as np
import matplotlib as plt
import cx_Oracle as co
import Credential as cd
import ALL_SQL as al
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', 200)
pd.set_option('display.max_rows', 100)




from IPython.display import display, HTML

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

def extract_data(trade, query, cob=0):
    ##Connect to the Databse
    cred = cd.POGB_CONSTR
    conn = co.connect(cred)
    if cob == 0:
        frame = pd.read_sql(query, params = {'trade_id':trade}, con = conn)
    else:
        frame = pd.read_sql(query, params = {'trade_id':trade, 
                                             'COB':cob}, con = conn)
    return frame

def extract_data_liq(query,trade,stream,cob):
    ##Connect to the Databse
    cred = cd.POLN_CONSTR
    conn = co.connect(cred)
    frame = pd.read_sql(query, params = {'trade_id':trade, 
                                         'app_installation':stream,
                                         'COB':cob}, con = conn)
    return frame

def extract_data_liq_more(query,trade,trad_trade_w, prime_trade_w,stream,cob):
    ##Connect to the Databse
    cred = cd.POLN_CONSTR
    conn = co.connect(cred)
    frame = pd.read_sql(query, params = {'trade_id':trade, 
                                         'trad_trade':trad_trade_w,
                                         'prim_trade':prime_trade_w,
                                         'app_installation':stream,
                                         'COB':cob}, con = conn)
    return frame

def extract_data_liq_else(query, alt_trad_id,trade, trad_trade_w, prime_trade_w, stream, cob):
    cred = cd.POLN_CONSTR
    conn = co.connect(cred)
    frame = pd.read_sql(query, params = {'alt_trad_id':alt_trad_id,
                                         'trade_id':trade, 
                                         'trad_trade':trad_trade_w,
                                         'prim_trade':prime_trade_w,
                                         'app_installation':stream,
                                         'COB':cob}, con = conn)
    return frame

def get_stream_sql(app_inst):
    switch = {
        'ANVLDN': al.ANV_SOURCE_TABLE_QUERY,
        'WSRLDN': al.WSS_SOURCE_TABLE_QUERY,
        'WSRMNH': al.WSS_SOURCE_TABLE_QUERY,
        'WSUROI': al.WSS_SOURCE_TABLE_QUERY,
        'WSNLDN': al.WSS_SOURCE_TABLE_QUERY,
        'WSUFAC': al.WSS_SOURCE_TABLE_QUERY,
        'WSUNIR': al.WSS_SOURCE_TABLE_QUERY,
        'LQSLDN': al.LQS_SOURCE_TABLE_QUERY,
        'CALLDN': al.CAL_SOURCE_TABLE_QUERY,
        'CALASP': al.CAL_SOURCE_TABLE_QUERY,
    }
    return switch.get(app_inst, al.ANV_SOURCE_TABLE_QUERY)

trade = input(color.BOLD + 'Enter the trade root contract ID: \n' +color.END)
cob = input(color.BOLD + 'Enter COB: ' + color.END + 
            '\nDate Format must be DD-MMM-YYYY eg. 13-OCT-2020: \n')
app_inst = input( color.BOLD + 'Enter Stream Name: ' + color.END + 
                 '\nStream Format should be in 6 letters eg. ANVLDN, LQSLDN, GDSLDN, CALV14: \n')

source_df = extract_data(trade,get_stream_sql(app_inst), cob)
atmb_df = extract_data(trade, al.ATM_BALS_QUERY, cob)

wh_df = extract_data(trade, al.WHCTD_query)
if len(wh_df) > 0:
    wh_df_slim = wh_df[wh_df['TRAD_APPLICATION_INSTALLATION'] == app_inst][['TRAD_ROOT_CONTRACT_ID','TRAD_TRADE_ID','TRAD_PRIMARY_CONTRACT_ID']]
    trade_id_w = wh_df_slim.iloc[0,0]
    trad_trade_w = str(wh_df_slim.iloc[0,1])
    prim_trad_w = wh_df_slim.iloc[0,2]
    
    lde_df = extract_data_liq(al.LDE_query, trade_id_w, app_inst,cob)
    wftf_df = extract_data_liq_more(al.WFTF_query, trade_id_w, trad_trade_w, prim_trad_w, app_inst, cob)
    wmld_df = extract_data_liq_more(al.WMLD_query, trade_id_w, trad_trade_w, prim_trad_w, app_inst, cob)
else:
    trade_id_w = trade# '0'
    trad_trade_w = '0'
    prim_trad_w = '0'

    lde_df = extract_data_liq(al.LDE_query, trade_id_w, app_inst,cob)
    wmld_df = extract_data_liq_more(al.WMLD_query, trade_id_w, trad_trade_w, prim_trad_w, app_inst, cob)
    
    if app_inst in ['WSRLDN','WSRMNH', 'WSUROI', 'WSNLDN', 'WSUFAC','WSUNIR']:
        try:
            alt_trad_id = source_df.loc[:1,'DEAL_NUMBER'].values[0]
            wftf_df = extract_data_liq_else(al.WFTF_query_2, alt_trad_id,trade_id_w, trad_trade_w, prim_trad_w, app_inst, cob)
        except:
            print('\n\nIt seems deal ID is not available in source table - or data is not available in source table.')
    else:
        trade_id_w = trade
        wftf_df = extract_data_liq_more(al.WFTF_query,trade_id_w, trad_trade_w, prim_trad_w, app_inst, cob)


h_df = pd.DataFrame( columns = ['WHCTD','SOURCE', 'ATM BAL', 'LDE', 'TROUBLESHOOT_F', 'MIBD'])
h_df.loc['IS AVAILABLE?'] = [len(wh_df),len(source_df),len(atmb_df),len(lde_df),len(wftf_df),len(wmld_df)]
h_df.loc['IS AVAILABLE?'] = h_df.loc['IS AVAILABLE?'].apply(lambda x: 'YES' if x>0 else 'NO')


print(color.BOLD + color.BLUE + color.UNDERLINE  + "\n\nHIGH LEVEL VIEW\n" + color.END ); display (h_df)
print(color.BOLD + color.BLUE + color.UNDERLINE  + "\n\nLIQ_DATA_EXTRACT\n" + color.END ); display(lde_df)
print(color.BOLD + color.BLUE + color.UNDERLINE  + "\n\nWH_FLM_TROUBLESHOOTING_F\n" + color.END ); display(wftf_df)
print(color.BOLD + color.BLUE + color.UNDERLINE  + "\n\nWH_MIB_LIQUIDITY_D\n" + color.END ); display(wmld_df)
print(color.BOLD + color.BLUE + color.UNDERLINE  + "\n\nSOURCE_TABLE\n" + color.END );display (source_df) 
print(color.BOLD + color.BLUE + color.UNDERLINE  + "\n\nWH_COMMON_TRADES_D\n" + color.END );display (wh_df) 
print(color.BOLD + color.BLUE + color.UNDERLINE  + "\n\nATM_BALANCES_F\n" + color.END );display (atmb_df) 

#sample root contrct id 103465588 - stream caldn sample date 29-JAN-2020 -- Bad Trade
#PJE4TLS2CUDVTEQ0LONP LQSLDN
