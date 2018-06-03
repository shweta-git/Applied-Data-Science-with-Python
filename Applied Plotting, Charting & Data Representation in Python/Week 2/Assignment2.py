
# coding: utf-8

# # Assignment 2
# 
# Before working on this assignment please read these instructions fully. In the submission area, you will notice that you can click the link to **Preview the Grading** for each step of the assignment. This is the criteria that will be used for peer grading. Please familiarize yourself with the criteria before beginning the assignment.
# 
# An NOAA dataset has been stored in the file `data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv`. The data for this assignment comes from a subset of The National Centers for Environmental Information (NCEI) [Daily Global Historical Climatology Network](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt) (GHCN-Daily). The GHCN-Daily is comprised of daily climate records from thousands of land surface stations across the globe.
# 
# Each row in the assignment datafile corresponds to a single observation.
# 
# The following variables are provided to you:
# 
# * **id** : station identification code
# * **date** : date in YYYY-MM-DD format (e.g. 2012-01-24 = January 24, 2012)
# * **element** : indicator of element type
#     * TMAX : Maximum temperature (tenths of degrees C)
#     * TMIN : Minimum temperature (tenths of degrees C)
# * **value** : data value for element (tenths of degrees C)
# 
# For this assignment, you must:
# 
# 1. Read the documentation and familiarize yourself with the dataset, then write some python code which returns a line graph of the record high and record low temperatures by day of the year over the period 2005-2014. The area between the record high and record low temperatures for each day should be shaded.
# 2. Overlay a scatter of the 2015 data for any points (highs and lows) for which the ten year record (2005-2014) record high or record low was broken in 2015.
# 3. Watch out for leap days (i.e. February 29th), it is reasonable to remove these points from the dataset for the purpose of this visualization.
# 4. Make the visual nice! Leverage principles from the first module in this course when developing your solution. Consider issues such as legends, labels, and chart junk.
# 
# The data you have been given is near **Ann Arbor, Michigan, United States**, and the stations the data comes from are shown on the map below.

# In[4]:

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


# #### 

# In[ ]:



