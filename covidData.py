import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import re
from boroughs import *
from cleanDate import *

# create dataframe with covid Data
def createDataFrame():
    file_name= 'data\COVID-19_Daily_Counts_of_Cases__Hospitalizations__and_Deaths.csv'
    df = pd.read_csv(file_name)
    boroList=['Bronx','Brooklyn','Staten Island','Manhattan','Queens']
    boroMap= {
        'Bronx':'BX',
        'Brooklyn': 'BK',
        'Staten Island': 'SI',
        'Manhattan': 'MN',
        'Queens': 'QN'
    }
    boroColumns= ['Date']
    # get the columns with borough information
    for boro in boroList:
        boroKey= r''+boroMap[boro]+'.+'
        isAvgCol= r'^.+AVG'
        for col in df.columns:
            if(re.match(boroKey,col) is not None and not re.match(isAvgCol,col)):
                # get the term associated with the borough: eg case count, death count, hospitalized
                term = re.findall(boroKey,col)[0].split('_')[1:]
                term = f'{term[0].title()} {term[1].title()}'
                neededCol= f'{boro}_{term}'
                
                df= df.rename(columns={
                    col:neededCol
                })
                boroColumns.append(neededCol)
                
            # is time measurement
            elif(col=='Year' or col=='Month' or col=='Date'):
                boroColumns.append(col)
    
    df= df.rename(columns={
        'DATE_OF_INTEREST':'Date'
    })
    df['Date'] = pd.to_datetime(df['Date'],format='%m/%d/%Y')
    return df[boroColumns].reset_index(drop=True)

# before we create helper functions, we should make one that provides the time measurement of the data.
def getTimeMeasure(dfColumns):
    cols=[]
    # has time measurement
    if('Date' in dfColumns):
        cols.append('Date')
        
    elif('Month' in dfColumns):
        cols.append('Month')
        cols.append('Year')
    return cols

# helper function to filterby cases, deaths, and hospitalized
def queryData(df: pd.DataFrame, query:str)->pd.DataFrame:
    queries= [
        'Case',
        'Hospitalized',
        'Death'
    ]
    if (query not in queries):
        raise ValueError(f'query \'{query}\' not in {queries}')
    
    query= query+' Count'
    
    queriedCols=getTimeMeasure(df.columns)
    key= r'.+'+query
    for col in df.columns:
        if (re.match(key,col)is not None):
            # get borough
            borough = col.split('_')[0]
            df= df.rename(columns={
                col:borough
            })
            queriedCols.append(borough)
            
    return df[queriedCols]

# helper function to filterby borough
def queryBoro(df:pd.DataFrame, boro:str):
    boro= boro.title()
    boroCols= getTimeMeasure(df.columns)
        
    for col in df.columns:
        if(boro in col):
            component =col.split('_')[1]
            df= df.rename(columns={
                col:component
            })
            boroCols.append(component)
    return df[boroCols].reset_index(drop=True)

# groups data into months
def monthlyData(df:pd.DataFrame)->pd.DataFrame:
    df['Date'] = pd.to_datetime(df['Date'],format='%m/%d/%Y')
    df['Month']= (df['Date'].dt.month).astype(str)
    df['Year'] = (df['Date'].dt.year).astype(str)
    df= df.groupby(['Year','Month']).sum().reset_index()
    df['Date'] =df['Month']+'-'+df['Year']
    return df

# Plotting timeline of daily cases
covidDataframe = createDataFrame()
covidCases= queryData(covidDataframe,'Case')

caseDF = pd.DataFrame()
for b in boroList:
    caseCount= covidCases[b].tolist()
    date= covidCases['Date'].tolist()
    for i in range(len(caseCount)):
        tempRow= pd.DataFrame({
            'Borough': b,
            'Cases' : caseCount[i],
            'Date': date[i]
        },index=[0])
        caseDF= pd.concat([caseDF,tempRow])
    
caseDF=caseDF.reset_index(drop=True)

plt.figure()
casePlot = sns.lineplot(
    data= caseDF,
    x='Date', y= 'Cases',
    hue= 'Borough',
    linewidth = .5
)
casePlot.set(yscale='log')
plt.title('New Cases by Day')
plt.xticks(rotation=45)
# plt.savefig(
#     "graphs/CovidCasesDaily.png",
#     bbox_inches="tight",
#     dpi=300,
#     transparent=True
# )
# plt.show()
plt.close()