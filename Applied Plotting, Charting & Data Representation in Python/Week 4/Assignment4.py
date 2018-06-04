import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


xl = pd.ExcelFile('Longitudinal Religious Congregations and Membership File, 1980-2010 (State Level).XLSX')
state = xl.parse(sheet_name='Sheet1')
state.drop(['STFIP', 'STATEAB', 'GRPCODE', 'CONGREG', 'RELTRAD', 'FAMILY', 'NOTE_MIS', 'NOTE_COM', 'NOTE_MEA'], axis=1,inplace=True)
state['ADHERENT%'] = state['ADHERENT']/state['TOTPOP'] * 100
state = state.groupby(['YEAR']).apply(lambda g: g.sort('ADHERENT%', ascending=False).head(5)).reset_index(level=[0,1], drop=True)

xl = pd.ExcelFile('Longitudinal Religious Congregations and Membership File, 1980-2010 (County Level).XLSX')
county = xl.parse(sheet_name='Sheet1')
county.drop(['FIPSMERG', 'CNTYNM', 'STATEAB', 'GRPCODE', 'CONGREG', 'RELTRAD', 'FAMILY', 'NOTE_MIS', 'NOTE_COM', 'NOTE_MEA'], axis=1, inplace=True)
county['ADHERENT%'] = county['ADHERENT']/county['TOTPOP'] * 100
county = county.groupby(['YEAR']).apply(lambda g: g.sort('ADHERENT%', ascending=False).head(5)).reset_index(level=[0,1], drop=True)

# Adding zeroed values to ensure same legends for botht the plots, this will enhance ease of comparison between the county and the state
state.loc[20] = [1980, 0,'Jewish Estimate (both conservatives, reformed, and orthodox)', 0, 0]
state.loc[21] = [1980, 0, 'Muslim Estimate', 0, 0]
state.loc[22] = [1980, 0, 'United Church of Christ', 0, 0]

county.loc[20] = [1980, 0, 'Lutheran Church, The Missouri Synod', 0, 0]

county.pivot(index='YEAR', columns='GRPNAME', values='ADHERENT%').plot.bar(stacked=True)#plot(kind='bar')
plt.legend(bbox_to_anchor=(1.25, 0.95))
plt.grid(linestyle='-')
plt.ylim([0,35])
ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.xaxis.grid(False)
ax.set_title('Top 5 Religious Congregation Adherents by Population% in Washtenaw County')

state.pivot(index='YEAR', columns='GRPNAME', values='ADHERENT%').plot.bar(stacked=True)#(kind='bar')
plt.legend(bbox_to_anchor=(1.25, 0.95))
plt.grid(linestyle='-')
ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.xaxis.grid(False)
ax.set_title('Top 5 Religious Congregation Adherents by Population% in Michigan State, USA')

plt.show()


# In[ ]:



