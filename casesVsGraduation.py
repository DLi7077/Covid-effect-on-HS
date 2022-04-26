"""_summary_
compares caseCount with 
"""

import pandas as pd
from attenVSgraduation import createDataframe
from covidData import caseDF
from boroughs import *
# Last day= June 27 (for 2022)
# every date that's before 6-27-year and after 6-27-(year-1)
# - shall be labeled as (year)

casesSchYear= pd.DataFrame()
for year in range(2020,2022):
  year= int(year)
  # set bounds that define the school year (including summer)
  lowerBound_date= (str(year-1)+'-6-27')
  upperBound_date= (str(year) + '-6-27')

  # extract case count
  dates= pd.to_datetime(caseDF['Date'])
  schoolTerm = caseDF[(dates>= lowerBound_date) & (dates< upperBound_date)]
  for boro in boroList:
    boroCases= schoolTerm.loc[schoolTerm['Borough']==boro]
    
    totalCases= boroCases['Cases'].sum()
    row= pd.DataFrame({
      'Borough': boro,
      'Cases': totalCases,
      'School Year': year 
    },index=[0])
    
    casesSchYear= pd.concat([casesSchYear,row])
casesSchYear= casesSchYear.reset_index(drop= True)

def get2020Cases(boro:str):
  return casesSchYear.loc[
    (casesSchYear['Borough']==boro) 
    &(casesSchYear['School Year']==2020) 
    ].values[0]


data2020= createDataframe('data/2020_DOE_High_School_Directory.csv',2020)
# data2020['cases']=data2020['Borough'].apply(get2020Cases)
cases2020= casesSchYear.loc[casesSchYear['School Year']==2020][['Borough','Cases']].reset_index(drop= True)

# df= data2020.merge(cases2020, on='Borough').reset_index(drop= True)

df= createDataframe('data/2021_DOE_High_School_Directory.csv',2021)

print(df)
