import pandas as pd
import re
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
    return df.reset_index()
    
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

# clean up date
from cleanDate import cleanDate
df = createDataFrame()
df= cleanData(df)

# exports
casesDF= cleanDate(caseData(df))
hospitalDF= cleanDate(hospitalData(df))
deathDF= cleanDate(deathData(df))
