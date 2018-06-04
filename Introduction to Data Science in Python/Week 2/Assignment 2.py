import pandas as pd

df = pd.read_csv('olympics.csv', index_col=0, skiprows=1)

for col in df.columns:
    if col[:2]=='01':
        df.rename(columns={col:'Gold'+col[4:]}, inplace=True)
    if col[:2]=='02':
        df.rename(columns={col:'Silver'+col[4:]}, inplace=True)
    if col[:2]=='03':
        df.rename(columns={col:'Bronze'+col[4:]}, inplace=True)
    if col[:1]=='№':
        df.rename(columns={col:'#'+col[1:]}, inplace=True)

names_ids = df.index.str.split('\s\(') # split the index by '('

df.index = names_ids.str[0] # the [0] element is the country name (new index) 
df['ID'] = names_ids.str[1].str[:3] # the [1] element is the abbreviation or ID (take first 3 characters from that)

df = df.drop('Totals')
df.head()

def answer_one():
    gold_max = df['Gold'].max()
    return df[df['Gold'] == gold_max].index[0]



def answer_two():
    diff = (df['Gold'] - df['Gold.1']).max()
    return df[df['Gold'] - df['Gold.1'] == diff].index[0]



def answer_three():
    df2 = df.copy()
    df2 = df2[(df2['Gold'] > 0) & (df2['Gold.1'] > 0) ]
    diff = ((df2['Gold'] - df2['Gold.1']) / df2['Gold.2']).max()
    return df2[((df2['Gold'] - df2['Gold.1']) / df2['Gold.2']) == diff].index[0]


def answer_four():
    df['Points'] = 3*df['Gold.2'] + 2*df['Silver.2'] + df['Bronze.2']
    return df['Points']



census_df = pd.read_csv('census.csv')
census_df.head()



def answer_five():
    df = census_df.copy()
    df = df[df['SUMLEV'] == 50]
    states = df['STNAME'].unique()
    state = states[0]
    maxcount = 0
    for s in states:
        ctycount = 0
        for d in df['STNAME'].iteritems():
            if d[1] == s:
                ctycount += 1
        if ctycount > maxcount:
            maxcount = ctycount
            state = s
    return state
answer_five()


def answer_six():
    df = census_df.copy()
    df = df[df['SUMLEV'] == 50]
    df = df.sort_values(by=['CENSUS2010POP'], ascending=False)
    df = df.groupby(['STNAME']).head([3])
    df = df.groupby(['STNAME']).sum()
    df = df.sort_values(by=['CENSUS2010POP'], ascending=False)
    return df.head(3).index.tolist()


def answer_seven():
    df = census_df.copy()
    df = df[df['SUMLEV'] == 50]
    columns_to_keep = ['STNAME','CTYNAME', 'POPESTIMATE2010', 'POPESTIMATE2011', 'POPESTIMATE2012', 'POPESTIMATE2013', 'POPESTIMATE2014', 'POPESTIMATE2015']
    df = df[columns_to_keep]
    return df.loc[(df.max(axis=1) - df.min(axis=1)).argmax()]['CTYNAME']



def answer_eight():
    df = census_df.copy()
    df = df[(df['SUMLEV'] == 50) & (df['REGION'] < 3) & df['CTYNAME'].str.startswith('Washington', na=False) & (df['POPESTIMATE2015'] > df['POPESTIMATE2014'])]
    return df[['STNAME', 'CTYNAME']]
answer_eight()



