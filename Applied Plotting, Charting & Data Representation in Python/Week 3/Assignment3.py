

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.cm as cm

y=42000

df = pd.DataFrame([np.random.normal(32000,200000,3650), 
                   np.random.normal(43000,100000,3650), 
                   np.random.normal(43500,140000,3650), 
                   np.random.normal(48000,70000,3650)], 
                  index=[1992,1993,1994,1995])

df['mean'] = df.mean(axis=1)
df['std'] = df.std(axis=1)
df['yerr'] = (df['std']/np.sqrt(df.shape[1]))*1.96
df['color'] = df.apply(lambda row:(row['mean'] - y)/row['std'], axis=1)
df['color'] = (df['color'] - df['color'].min())/(df['color'].max()-df['color'].min())

colors = [(0, 0, 1), (1, 1, 1), (1, 0, 0)]
color_map = mcolors.LinearSegmentedColormap.from_list('bar', colors, N=11)
color_bar = cm.ScalarMappable(cmap=color_map)
color_bar.set_array([])

pos = np.arange(len(df.index.values))

fig = plt.figure()
plt.bar(pos, df['mean'], yerr=df['yerr'], color=color_bar.to_rgba(df['color']), edgecolor='black')
plt.colorbar(color_bar, orientation='horizontal')
plt.xticks(pos, df.index.values)
plt.axhline(y=y, color='grey', linestyle='-')
plt.annotate('y = {}'.format(y), xy=(0,y), xytext =(300,10), textcoords='offset points')

def onclick(event):
    new_y = event.ydata
    plt.cla()
    df['color'] = df.apply(lambda row:(row['mean'] - new_y)/row['std'], axis=1)
    df['color'] = (df['color'] - df['color'].min())/(df['color'].max()-df['color'].min())
    plt.bar(pos, df['mean'], yerr=df['yerr'], color=color_bar.to_rgba(df['color']), edgecolor='black')
    plt.axhline(y=new_y, color='grey', linestyle='-')
    plt.annotate('y = {}'.format(new_y), xy=(0,new_y), xytext =(300,10), textcoords='offset points')
    
plt.gcf().canvas.mpl_connect('button_press_event', onclick)





