

import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd
import numpy as np

def leaflet_plot_stations(binsize, hashid):

    df = pd.read_csv('data/C2A2_data/BinSize_d{}.csv'.format(binsize))

    station_locations_by_hash = df[df['hash'] == hashid]

    lons = station_locations_by_hash['LONGITUDE'].tolist()
    lats = station_locations_by_hash['LATITUDE'].tolist()

    plt.figure(figsize=(8,8))

    plt.scatter(lons, lats, c='r', alpha=0.7, s=200)

    return mplleaflet.display()

leaflet_plot_stations(400,'fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89')
df = pd.read_csv('data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv')

df['YYYY'] = df['Date'].apply(lambda row: row[:4])
df['MM-DD'] = df['Date'].apply(lambda row: row[5:])

df = df[df['MM-DD'] != '02-29']

dfmin = df[(df['YYYY'] != '2015')].groupby('MM-DD').agg({'Data_Value': np.min})
dfmax = df[(df['YYYY'] != '2015')].groupby('MM-DD').agg({'Data_Value': np.max})

dfmin2015 = df[(df['YYYY'] == '2015')].groupby('MM-DD').agg({'Data_Value': np.min})
dfmax2015 = df[(df['YYYY'] == '2015')].groupby('MM-DD').agg({'Data_Value': np.max})

recordlow_broken = np.where(dfmin2015['Data_Value'] < dfmin['Data_Value'])[0]
recordhigh_broken = np.where(dfmax2015['Data_Value'] > dfmax['Data_Value'])[0]

plt.figure(figsize=(17,7))
plt.plot(dfmin.values/10, 'blue', label='Record Low (2005-2014)', alpha=0.5)
plt.plot(dfmax.values/10, 'red', label='Record High (2005-2014)', alpha=0.5)
plt.xlabel('Month')
plt.ylabel('Temperature ($^\circ$C)')
plt.title('Daily Temperature Records near Ann Arbor, Michigan (US)')
plt.xticks(np.linspace(15,15 + 30*11 , num = 12), (r'Jan', r'Feb', r'Mar', r'Apr', r'May', r'Jun', r'Jul', r'Aug', r'Sep', r'Oct', r'Nov', r'Dec') )
ax = plt.gca()
ax.axis([0,365,-37.0, 41.0])

ax.fill_between(range(len(dfmin['Data_Value'])), 
                       dfmin['Data_Value']/10, dfmax['Data_Value']/10, 
                       facecolor='grey', 
                       alpha=0.25)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
    
plt.scatter(recordlow_broken, dfmin.iloc[recordlow_broken]/10, s=50, c='blue', label='Record Low Broken (2015)', alpha=0.6)
for i in range(0, recordlow_broken.shape[0]):
    plt.annotate(dfmin.iloc[recordlow_broken].index[i], xy=(recordlow_broken[i], dfmin.iloc[recordlow_broken[i]]/10), 
                 xytext=(10,-40), color='blue',textcoords='offset points', ha='center', va='bottom',
            bbox=dict(boxstyle='round,pad=0.2', fc='yellow', alpha=0.5),
            arrowprops=dict(arrowstyle='->', color='blue'))


plt.scatter(recordhigh_broken, dfmax.iloc[recordhigh_broken]/10, s=50, c='red', label='Record High Broken (2015)', alpha=0.6)
for i in range(0, recordhigh_broken.shape[0]):
    plt.annotate(dfmax.iloc[recordhigh_broken].index[i], xy=(recordhigh_broken[i], dfmax.iloc[recordhigh_broken[i]]/10), 
                 xytext=(10,-30), color='red',textcoords='offset points', ha='center', va='bottom',
            bbox=dict(boxstyle='round,pad=0.2', fc='yellow', alpha=0.5),
            arrowprops=dict(arrowstyle='->', color='red'))

plt.tick_params(top='off', right='off', labelleft='on', labelbottom='on')
plt.legend(frameon=False)
plt.show()



