
import pandas as pd
import numpy as np
from scipy.stats import ttest_ind

states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}

def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    columns=["State", "RegionName"]  )
    
    The following cleaning needs to be done:

    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.
    3. Depending on how you read the data, you may need to remove newline character '\n'. '''
    
    df = pd.read_csv('university_towns.txt', sep="\n", header=None, names=['RegionName'])
    df['is_state'] = df['RegionName'].str.contains('\[edit\]')
    df['RegionName'] = df['RegionName'].str.replace('\[.*', '')
    df['RegionName'] = df['RegionName'].str.replace('\s\(.*', '')
    for row in df.itertuples():
        if (row[2]):
            state = row[1]
        else:
            df.set_value(row[0], 'State', state)
    df = df[df['is_state']==False]
    df.drop(['is_state'], axis=1, inplace=True)
    df = df[['State', 'RegionName']]
    df.reset_index(inplace=True)
    df.drop(['index'], axis=1, inplace=True)
   
    return df

def get_recession_start():
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''
    xl = pd.ExcelFile('gdplev.xls')
    gdp = xl.parse(sheet_name='Sheet1', header=6)
    gdp = gdp.iloc[:,[4,6]]
    gdp.rename(columns={'Unnamed: 4': 'Quarter', 'Unnamed: 6': 'GDP'}, inplace=True)
    gdp = gdp[gdp['Quarter'] >= '2000q1']
   
    gdp.reset_index(inplace=True)
    gdp.drop(['index'], axis=1, inplace=True)
    gdp['RecessionStart'] = gdp[0:64].apply(lambda row:True if ((gdp.iloc[row.name+1]['GDP'] < gdp.iloc[row.name]['GDP']) & (gdp.iloc[row.name+2]['GDP'] < gdp.iloc[row.name+1]['GDP'])) else False, axis=1)
    return gdp[gdp['RecessionStart'] == True]['Quarter'].values[1]


def get_recession_end():
    '''Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3'''
    xl = pd.ExcelFile('gdplev.xls')
    gdp = xl.parse(sheet_name='Sheet1', header=6)
    gdp = gdp.iloc[:,[4,6]]
    gdp.rename(columns={'Unnamed: 4': 'Quarter', 'Unnamed: 6': 'GDP'}, inplace=True)
    gdp = gdp[gdp['Quarter'] >= '2000q1']
   
    gdp.reset_index(inplace=True)
    gdp.drop(['index'], axis=1, inplace=True)
    recession_start = get_recession_start()
    gdp['RecessionEnd'] = gdp[2:66].apply(lambda row:True if ((gdp.iloc[row.name-1]['GDP'] < gdp.iloc[row.name]['GDP']) & (gdp.iloc[row.name-2]['GDP'] < gdp.iloc[row.name-1]['GDP']) & (gdp.iloc[row.name]['Quarter'] > recession_start)) else False, axis=1)
    return gdp[gdp['RecessionEnd'] == True]['Quarter'].values[0]

def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3'''
    recession_start = get_recession_start()
    recession_end = get_recession_end()
    xl = pd.ExcelFile('gdplev.xls')
    gdp = xl.parse(sheet_name='Sheet1', header=6)
    gdp = gdp.iloc[:,[4,6]]
    gdp.rename(columns={'Unnamed: 4': 'Quarter', 'Unnamed: 6': 'GDP'}, inplace=True)
    gdp = gdp[gdp['Quarter'] >= '2000q1']
    gdp.reset_index(inplace=True)
    gdp.drop(['index'], axis=1, inplace=True)
    
    df = gdp[(gdp['Quarter']>=recession_start) & (gdp['Quarter']<=recession_end)]
    return df[df['GDP'] == df['GDP'].min()]['Quarter'].values[0]

def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].
    
    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.
    
    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''
    df = pd.read_csv('City_Zhvi_AllHomes.csv')
    df['State'] = df['State'].apply(lambda row:states[row])
    df = df.set_index(['State', 'RegionName'])
    df.drop(df.columns[df.columns.get_loc('1996-04'):df.columns.get_loc('1999-12') + 1], axis=1, inplace=True)
    
    for year in range(2000,2016):
        for quarter in range(1,5):
            column_name = '{}q{}'.format(year,quarter)
            seed = quarter*3
            df[column_name] = (df['{}-{}'.format(year, str(seed).zfill(2))] + df['{}-{}'.format(year, str(seed-1).zfill(2))] + df['{}-{}'.format(year, str(seed-2).zfill(2))])/3   
    
    for quarter in range(1,4):
        column_name = '{}q{}'.format(2016,quarter)
        seed = quarter*3
        df[column_name] = (df['{}-{}'.format(year, str(seed).zfill(2))] + df['{}-{}'.format(year, str(seed-1).zfill(2))] + df['{}-{}'.format(year, str(seed-2).zfill(2))])/3   
    
    df.drop(df.columns[df.columns.get_loc('2000-01'):df.columns.get_loc('2016-08') + 1], axis=1, inplace=True)
    df.drop(df.columns[0:4], axis=1, inplace=True)
    return df


def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 
    
    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if 
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''
    
    df_housing = convert_housing_data_to_quarters()
    recession_start = get_recession_start()
    recession_bottom =  get_recession_bottom()
    df_housing.drop(df_housing.columns[:df_housing.columns.get_loc(recession_start)-1], axis=1, inplace=True)
    df_housing.drop(df_housing.columns[df_housing.columns.get_loc(recession_bottom):], axis=1, inplace=True)
    
    df_university = get_list_of_university_towns()
    
    df_housing_university = pd.merge(df_university, df_housing.reset_index(), how='inner')
    df_housing_university['price_ratio'] = df_housing_university.ix[:,2]/df_housing_university.ix[:,-1]
   
    df_housing_non_university = pd.merge(df_university, df_housing.reset_index(),indicator=True, how='outer').query('_merge=="right_only"').drop('_merge', axis=1)
    df_housing_non_university['price_ratio'] = df_housing_non_university.ix[:,2]/df_housing_non_university.ix[:,-1]
    
    statistic, pvalue = tuple(ttest_ind(df_housing_university['price_ratio'].dropna() , df_housing_non_university['price_ratio'].dropna()))
    statistic = statistic<0
    
    return (pvalue<0.01, pvalue, ['non-university town', 'university town'][statistic])

