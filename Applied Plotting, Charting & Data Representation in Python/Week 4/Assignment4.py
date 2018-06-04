
# coding: utf-8

# # Assignment 4
# 
# Before working on this assignment please read these instructions fully. In the submission area, you will notice that you can click the link to **Preview the Grading** for each step of the assignment. This is the criteria that will be used for peer grading. Please familiarize yourself with the criteria before beginning the assignment.
# 
# This assignment requires that you to find **at least** two datasets on the web which are related, and that you visualize these datasets to answer a question with the broad topic of **religious events or traditions** (see below) for the region of **Ann Arbor, Michigan, United States**, or **United States** more broadly.
# 
# You can merge these datasets with data from different regions if you like! For instance, you might want to compare **Ann Arbor, Michigan, United States** to Ann Arbor, USA. In that case at least one source file must be about **Ann Arbor, Michigan, United States**.
# 
# You are welcome to choose datasets at your discretion, but keep in mind **they will be shared with your peers**, so choose appropriate datasets. Sensitive, confidential, illicit, and proprietary materials are not good choices for datasets for this assignment. You are welcome to upload datasets of your own as well, and link to them using a third party repository such as github, bitbucket, pastebin, etc. Please be aware of the Coursera terms of service with respect to intellectual property.
# 
# Also, you are welcome to preserve data in its original language, but for the purposes of grading you should provide english translations. You are welcome to provide multiple visuals in different languages if you would like!
# 
# As this assignment is for the whole course, you must incorporate principles discussed in the first week, such as having as high data-ink ratio (Tufte) and aligning with Cairo’s principles of truth, beauty, function, and insight.
# 
# Here are the assignment instructions:
# 
#  * State the region and the domain category that your data sets are about (e.g., **Ann Arbor, Michigan, United States** and **religious events or traditions**).
#  * You must state a question about the domain category and region that you identified as being interesting.
#  * You must provide at least two links to available datasets. These could be links to files such as CSV or Excel files, or links to websites which might have data in tabular form, such as Wikipedia pages.
#  * You must upload an image which addresses the research question you stated. In addition to addressing the question, this visual should follow Cairo's principles of truthfulness, functionality, beauty, and insightfulness.
#  * You must contribute a short (1-2 paragraph) written justification of how your visualization addresses your stated research question.
# 
# What do we mean by **religious events or traditions**?  For this category you might consider calendar events, demographic data about religion in the region and neighboring regions, participation in religious events, or how religious events relate to political events, social movements, or historical events.
# 
# ## Tips
# * Wikipedia is an excellent source of data, and I strongly encourage you to explore it for new data sources.
# * Many governments run open data initiatives at the city, region, and country levels, and these are wonderful resources for localized data sources.
# * Several international agencies, such as the [United Nations](http://data.un.org/), the [World Bank](http://data.worldbank.org/), the [Global Open Data Index](http://index.okfn.org/place/) are other great places to look for data.
# * This assignment requires you to convert and clean datafiles. Check out the discussion forums for tips on how to do this from various sources, and share your successes with your fellow students!
# 
# ## Example
# Looking for an example? Here's what our course assistant put together for the **Ann Arbor, MI, USA** area using **sports and athletics** as the topic. [Example Solution File](./readonly/Assignment4_example.pdf)

# In[39]:

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



