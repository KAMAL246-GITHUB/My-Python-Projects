import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.animation as animation
from IPython.display import HTML
pd.options.mode.chained_assignment = None
%matplotlib inline


df = pd.read_excel('FS_Incident_2019.xlsx')
df1= df[['Department','Owning Team','Month','Incident Number' ]]
df1['Month'] = pd.to_datetime(df1['Month']).dt.strftime('%b')
df1.rename(columns = {'Incident Number':'Count','Owning Team': 'Team', 'Department':'Dept' }, inplace = True)
df2 = df1.groupby(['Dept','Team','Month'])['Count']\
    .count()\
    .to_frame()\
    .reset_index()
colors = dict(zip(
    ['Accounting', 'EPM', 'Reporting'],
    [ "red", "steelblue","green"]
))
group_lk = df2.set_index('Team')['Dept'].to_dict()

fig, ax = plt.subplots(figsize=(15, 8))
plt.style.use('bmh')

def draw_barchart(month):    
    dff = df2[df2['Month'].eq(month)].sort_values(by = 'Count')
    
    ax.clear()
    ax.barh(dff['Team'], dff['Count'], color=[colors[group_lk[x]] for x in dff['Team']])
    dx = dff['Count'].max() / 200
    for i, (Count, Team) in enumerate(zip(dff['Count'], dff['Team'])):
        ax.text(-0.4, i,     Team,           size=12, ha='right', va='bottom')
        ax.text(-10, i-.25, group_lk[Team], size=12, color='#444444', ha='right', va='baseline')
        ax.text(Count+dx, i,     f'{Count:,.0f}',  size=14, ha='left',  va='center')
        
       

    ax.text(0.8, 0.4, month, transform=ax.transAxes, color='#777777', size=30, ha='right', weight=600)
    ax.text(0, 1.06, 'Incident Count', transform=ax.transAxes, size=12, color='#777777')
    ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    ax.xaxis.set_ticks_position('top')
    ax.tick_params(axis='x', colors='#777777', labelsize=12)
    ax.set_yticks([])
    ax.margins(0, 0.01)
    ax.grid(which='major', axis='both', linestyle='-')
    ax.set_axisbelow(True)
    ax.text(0, 1.15, 'The most incident producing team Jan - Oct 2019',
            transform=ax.transAxes, size=14, weight=400, ha='left', va='top')
    ax.text(1, 0, 'by @Kamal; credit @pratapvardhan and @jburnmurdoch', transform=ax.transAxes, color='#777777', ha='right',
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='white'))
    fig.subplots_adjust(left = 0.16)
#     plt.tight_layout()
#     plt.box(False)
    

    

    
animator = animation.FuncAnimation(fig, draw_barchart, 
                                   frames=['Jan','Feb','Mar','Apr','May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct'], 
                                   interval = 400)
HTML(animator.to_jshtml())
