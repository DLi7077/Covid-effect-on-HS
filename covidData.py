import matplotlib
import pandas as pd
import re

from pyparsing import col
from boroughs import boroughList

# create dataframe
#borough filters
def createDataFrame():
    file_name= 'data\COVID-19_Daily_Counts_of_Cases__Hospitalizations__and_Deaths.csv'
    df = pd.read_csv(file_name)
    return df
# clean data: return df
def cleanData(df: pd.DataFrame)-> pd.DataFrame:
    boroList=['Bronx','Brooklyn','Staten Island','Manhattan','Queens']
    boroMap= {
        'Bronx':'BX',
        'Brooklyn': 'BK',
        'Staten Island': 'SI',
        'Manhattan': 'MN',
        'Queens': 'QN'
    }
    df['DATE_OF_INTEREST'] = pd.to_datetime(df['DATE_OF_INTEREST'])
    dates= df['DATE_OF_INTEREST']
    boroColumns= ['DATE_OF_INTEREST']
    # get the needed columns
    for boro in boroList:
        boroKey= r''+boroMap[boro]+'.+'
        isAvgCol= r'^.+AVG'
        for colName in df.columns:
            if(re.match(boroKey,colName) is not None
                and not re.match(isAvgCol,colName)):
                boroColumns.append(colName)
    df= df[boroColumns]
    
    # now aggregate the sum for each col
    df['Year']= dates.dt.year
    df['Month']=dates.dt.month
    df= df.groupby(['Year','Month']).sum()
    return df.reset_index(drop= True)
    
# get case count for each borough
def caseData(df:pd.DataFrame):
    columns =['Year','Month']
    key= r'.+CASE_COUNT'
    for c in df.columns:
        if (re.match(key,c)is not None):
            columns.append(c) 
    df= df[columns]
    df.columns= ['Year','Month','Bronx','Brooklyn','Staten Island','Manhattan','Queens']
    
    return df

# get case count for each borough
def hospitalData(df:pd.DataFrame):
    columns =['Year','Month']
    key= r'.+HOSPITALIZED_COUNT'
    for c in df.columns:
        if (re.match(key,c)is not None):
            columns.append(c) 
    df= df[columns]
    df.columns= ['Year','Month','Bronx','Brooklyn','Staten Island','Manhattan','Queens']
    
    return df

# get case count for each borough
def deathData(df:pd.DataFrame):
    columns =['Year','Month']
    key= r'.+DEATH_COUNT'
    for c in df.columns:
        if (re.match(key,c)is not None):
            columns.append(c)
    df= df[columns]
    df.columns= ['Year','Month','Bronx','Brooklyn','Staten Island','Manhattan','Queens']
    
    return df

# get borough data
def boroData(df:pd.DataFrame, boro:str):
    br= boro.title()
    if(br not in boroughList): return
    cols=['Year','Month',br]
    return df[cols]

# get the totalCaseCount of a given covid df
def totalCaseCount(df: pd.DataFrame)-> int:
    caseCountCols=[]
    regex= r'.+CASE_COUNT' # to match columns that contain cases
    for colName in df.columns:
        if(colName=='CASE_COUNT'): #Case_count will exist if boroughs not filtered
            caseCountCols= ['CASE_COUNT']
            break
        elif(re.match(regex,colName) is not None):
            caseCountCols.append(colName)
    totalCases= 0
    for col in caseCountCols:
        totalCases+= df[col].sum()
    return totalCases

def datawDay():
    df= createDataFrame()
    boroList=['Bronx','Brooklyn','Staten Island','Manhattan','Queens']
    boroMap= {
        'Bronx':'BX',
        'Brooklyn': 'BK',
        'Staten Island': 'SI',
        'Manhattan': 'MN',
        'Queens': 'QN'
    }
    df['DATE_OF_INTEREST'] = pd.to_datetime(df['DATE_OF_INTEREST'])
    dates= df['DATE_OF_INTEREST']
    boroColumns= ['DATE_OF_INTEREST']
    # get the needed columns
    for boro in boroList:
        boroKey= r''+boroMap[boro]+'.+'
        isAvgCol= r'^.+AVG'
        for colName in df.columns:
            if(re.match(boroKey,colName) is not None
                and not re.match(isAvgCol,colName)):
                boroColumns.append(colName)
    df= df[boroColumns]
    df= df.rename(columns={'DATE_OF_INTEREST':'Date'})
    return df

# print(datawDay())
def filterBy(df, cate= 'CASE'):
    caseCols= ['Date']
    key= r'.+'+cate
    for cols in df.columns:
        if (re.match(key,cols) is not None):
            caseCols.append(cols)
    
    # print(df.columns)
    df= df[caseCols]
    df= df.rename(columns={
        'BX_CASE_COUNT': 'Bronx',
        'BK_CASE_COUNT': 'Brooklyn',
        'SI_CASE_COUNT': 'Staten Island',
        'MN_CASE_COUNT': 'Manhattan',
        'QN_CASE_COUNT': 'Queens'
        })
    return df


# clean up date
from cleanDate import cleanDate
df = createDataFrame()
df= cleanData(df)

# exports
cases= cleanDate(caseData(df))
caseWDay= filterBy(datawDay())
hospitalDF= cleanDate(hospitalData(df))
deathDF= cleanDate(deathData(df))

# reorganize the data
caseDF = pd.DataFrame()
from boroughs import bList
for b in bList:
    caseCount= caseWDay[b].tolist()
    date= caseWDay['Date'].tolist()
    for i in range(len(caseCount)):
        tempRow= pd.DataFrame({
            'Borough': b,
            'Cases' : caseCount[i],
            'Date': date[i]
        },index=[0])
        caseDF= pd.concat([caseDF,tempRow])
    
caseDF=caseDF.reset_index(drop=True)

import seaborn as sns
import matplotlib.pyplot as plt

plt.figure()
casePlot = sns.lineplot(
    data= caseDF,
    x='Date', y= 'Cases',
    hue= 'Borough',
)
casePlot.set(yscale='log')
plt.title('New Cases by Day')
plt.xticks(rotation=45)
plt.savefig(
    "graphs/CovidCasesDaily.png",
    bbox_inches="tight",
    dpi=300,
    transparent=True
)
plt.close()