import pandas as pd
import re
#borough filters

# Borough filters: return df
def boroCovidData(df: pd.DataFrame, boro: str)-> pd.DataFrame:
    boro = boro.lower() #lowercase so its not case sensitive
    boroList=['bronx','brooklyn','staten island','manhattan','queens']
    
    if(not boro in boroList):
        print(boro, 'is an invalid borough')
        print('expected:\n', boroList)
        quit()
    
    boroMap= {
        'bronx':'BX',
        'brooklyn': 'BK',
        'staten island': 'SI',
        'manhattan': 'MN',
        'queens': 'QN'
    }
    
    boroKey= r''+boroMap[boro]+'.+'
    isAvgCol= r'^.+AVG'
    boroColumns= ['DATE_OF_INTEREST']
    for colName in df.columns:
        if(re.match(boroKey,colName) is not None
           and not re.match(isAvgCol,colName)):
            boroColumns.append(colName)
    return df[boroColumns]

# params: 
#   df: a dataframe with a 'DATE_OF_INTEREST' and '.._CASE_COUNT' columns
#   year: integer representing year
# returns:
#   the amount of cases at the end of the given school year
# instead of ending at 12-21-XXXX, it will end at June-27-XXXX
# 2022 Term Calendar: https://www.schools.nyc.gov/about-us/news/2021-2022-school-year-calendar
def casesOfSchoolYear(df: pd.DataFrame, year: int)-> int:
    year= int(year)
    if(int(year)<2019): # no cases prior to 2020
        print('NOTE: Covid-19 Cases appeared in 2020')
        return 0
    
    # set bounds that define the school year (including summer)
    lowerBound_date= (str(year-1)+'-6-27')
    upperBound_date= (str(year) + '-6-27')
    
    # extract case count
    dates= pd.to_datetime(df['DATE_OF_INTEREST'])
    schoolTerm = df[(dates>= lowerBound_date) & (dates< upperBound_date)]
    
    return schoolTerm['BX_CASE_COUNT'].sum()

