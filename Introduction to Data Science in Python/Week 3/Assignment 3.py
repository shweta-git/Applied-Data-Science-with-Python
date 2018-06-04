
import pandas as pd
def answer_one():
    xl = pd.ExcelFile('Energy Indicators.xls')
    energy = xl.parse(sheet_name='Energy',skiprows=16, skip_footer=38)
    energy.drop(['Unnamed: 0', 'Unnamed: 1'], axis=1, inplace=True)
    energy.drop(0, inplace=True)
    energy.rename(columns={'Unnamed: 2': 'Country', 'Energy Supply per capita': 'Energy Supply per Capita','Renewable Electricity Production': '% Renewable'}, inplace=True)
    energy['Energy Supply'] = energy.apply(lambda row:row['Energy Supply']*1000000 if (type(row['Energy Supply'])==int) else None  , axis=1)
    energy['Country'] = energy['Country'].str.replace('\d+', '')
    energy['Country'] = energy['Country'].str.replace('\s\(.*\)', '')
    energy['Country'].replace(to_replace=['Republic of Korea', 'United States of America', 'United Kingdom of Great Britain and Northern Ireland', 'China, Hong Kong Special Administrative Region'], value=['South Korea', 'United States', 'United Kingdom', 'Hong Kong'], inplace=True)
    
    GDP = pd.read_csv('world_bank.csv', header=4)
    GDP['Country Name'].replace(to_replace=['Korea, Rep.', 'Iran, Islamic Rep.', 'Hong Kong SAR, China'], value=['South Korea', 'Iran', 'Hong Kong'], inplace=True)
    GDP.rename(columns={'Country Name': 'Country'}, inplace=True)
    xls = pd.ExcelFile('scimagojr-3.xlsx')
    ScimEn = xls.parse(sheet_name='Sheet1')
    
    df = pd.merge(ScimEn[:15], pd.merge(energy, GDP[['Country','2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']], how='inner', left_on='Country', right_on ='Country'), how='inner', left_on='Country', right_on ='Country')
    df.set_index(['Country'], inplace=True)
    return df

get_ipython().run_cell_magic('HTML', '', '<svg width="800" height="300">\n  <circle cx="150" cy="180" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="blue" />\n  <circle cx="200" cy="100" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="red" />\n  <circle cx="100" cy="100" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="green" />\n  <line x1="150" y1="125" x2="300" y2="150" stroke="black" stroke-width="2" fill="black" stroke-dasharray="5,3"/>\n  <text  x="300" y="165" font-family="Verdana" font-size="35">Everything but this!</text>\n</svg>')

def answer_two():
    xl = pd.ExcelFile('Energy Indicators.xls')
    energy = xl.parse(sheet_name='Energy',skiprows=16, skip_footer=38)
    energy.drop(['Unnamed: 0', 'Unnamed: 1'], axis=1, inplace=True)
    energy.drop(0, inplace=True)
    energy.rename(columns={'Unnamed: 2': 'Country', 'Energy Supply per capita': 'Energy Supply per Capita','Renewable Electricity Production': '% Renewable'}, inplace=True)
    energy['Energy Supply'] = energy.apply(lambda row:row['Energy Supply']*1000000 if (type(row['Energy Supply'])==int) else None  , axis=1)
    energy['Country'] = energy['Country'].str.replace('\d+', '')
    energy['Country'] = energy['Country'].str.replace('\s\(.*\)', '')
    energy['Country'].replace(to_replace=['Republic of Korea', 'United States of America', 'United Kingdom of Great Britain and Northern Ireland', 'China, Hong Kong Special Administrative Region'], value=['South Korea', 'United States', 'United Kingdom', 'Hong Kong'], inplace=True)
    
    GDP = pd.read_csv('world_bank.csv', header=4)
    GDP['Country Name'].replace(to_replace=['Korea, Rep.', 'Iran, Islamic Rep.', 'Hong Kong SAR, China'], value=['South Korea', 'Iran', 'Hong Kong'], inplace=True)
    GDP.rename(columns={'Country Name': 'Country'}, inplace=True)
    xls = pd.ExcelFile('scimagojr-3.xlsx')
    ScimEn = xls.parse(sheet_name='Sheet1')
    
    df = pd.merge(ScimEn, pd.merge(energy, GDP[['Country','2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']], how='inner', left_on='Country', right_on ='Country'), how='inner', left_on='Country', right_on ='Country')
    dfall = pd.merge(ScimEn, pd.merge(energy, GDP[['Country','2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']], how='outer', left_on='Country', right_on ='Country'), how='outer', left_on='Country', right_on ='Country')

    return len(dfall) - len(df)


def answer_three():
    df = answer_one()
    avgGDP = df[['2006','2007','2008','2009','2010','2011','2012','2013','2014','2015']].mean(skipna=True, axis=1).sort_values(ascending=False)
    return avgGDP

def answer_four():
    df15 = answer_one()
    df15['avgGDP'] = answer_three()
    df15.sort(['avgGDP'], ascending=[0], inplace=True)
    return df15.iloc[5]['2015'] - df15.iloc[5]['2006'] 


def answer_five():
    df15 = answer_one()
    avgEnergySupply = df15['Energy Supply per Capita'].astype('float').mean()
    return avgEnergySupply


def answer_six():
    df15 = answer_one()
    country = df15[df15['% Renewable'] == df15['% Renewable'].max()].index[0]
    return (country, df15['% Renewable'].max())


def answer_seven():
    df15 = answer_one()
    df15['ratio'] = df15['Self-citations']/df15['Citations']
    country = df15[df15['ratio'] == df15['ratio'].max()].index[0]
    return (country, df15['ratio'].max())



def answer_eight():
    df15 = answer_one()
    df15['Population'] = df15['Energy Supply']/df15['Energy Supply per Capita']
    df15.sort(['Population'], ascending=[0], inplace=True)
    return df15.index[2]

import numpy as np
def answer_nine():
    df15 = answer_one()
    df15['Population'] = df15['Energy Supply']/df15['Energy Supply per Capita']
    df15['Citable docs per Capita'] = df15['Citable documents']/df15['Population']
    df15['Citable docs per Capita'] = np.float64(df15['Citable docs per Capita'])
    df15['Energy Supply per Capita'] = np.float64(df15['Energy Supply per Capita'])
    corr = df15['Citable docs per Capita'].corr(df15['Energy Supply per Capita'])
    return corr

def plot9():
    import matplotlib as plt
    get_ipython().magic('matplotlib inline')
    
    Top15 = answer_one()
    Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    Top15['Citable docs per Capita'] = Top15['Citable documents'] / Top15['PopEst']
    Top15.plot(x='Citable docs per Capita', y='Energy Supply per Capita', kind='scatter', xlim=[0, 0.0006])


def answer_ten():
    df15 = answer_one()
    medianRenew = df15['% Renewable'].median()
    df15['HighRenew'] = df15.apply(lambda row:1 if row['% Renewable'] >= medianRenew else 0, axis=1)
    df15.sort(['Rank'], ascending=[1])
    return df15['HighRenew']

import numpy as np
def answer_eleven():
    df15 = answer_one()
    df15['Population'] = df15['Energy Supply'].astype(float)/df15['Energy Supply per Capita']
    df15['Population'] = np.float64( df15['Population'])
    ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
    df15['Continent'] = df15.apply(lambda row:ContinentDict[row.name], axis=1)
    df = df15.set_index('Continent').groupby(level=0)['Population'].agg({'size':np.size, 'sum':np.sum, 'mean': np.mean, 'std': np.std})
    return df


def answer_twelve():
    df15 = answer_one()
    ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
    df15['Continent'] = df15.apply(lambda row:ContinentDict[row.name], axis=1)
    df15['Bin'] = pd.cut(df15['% Renewable'], 5)
    df = df15.groupby(['Continent', 'Bin'])
    return df.size()



def answer_thirteen():
    df15 = answer_one()
    df15['PopEst'] = df15['Energy Supply'].astype(float)/df15['Energy Supply per Capita']
    df15['PopEst'] = df15['PopEst'].map('{:,}'.format)
    return  df15['PopEst']
answer_thirteen()



def plot_optional():
    import matplotlib as plt
    get_ipython().magic('matplotlib inline')
    Top15 = answer_one()
    ax = Top15.plot(x='Rank', y='% Renewable', kind='scatter', 
                    c=['#e41a1c','#377eb8','#e41a1c','#4daf4a','#4daf4a','#377eb8','#4daf4a','#e41a1c',
                       '#4daf4a','#e41a1c','#4daf4a','#4daf4a','#e41a1c','#dede00','#ff7f00'], 
                    xticks=range(1,16), s=6*Top15['2014']/10**10, alpha=.75, figsize=[16,6]);

    for i, txt in enumerate(Top15.index):
        ax.annotate(txt, [Top15['Rank'][i], Top15['% Renewable'][i]], ha='center')

    print("This is an example of a visualization that can be created to help understand the data. This is a bubble chart showing % Renewable vs. Rank. The size of the bubble corresponds to the countries' 2014 GDP, and the color corresponds to the continent.")

