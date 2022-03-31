from tracemalloc import start
import pandas as pd
import covidData as Covid
import highschoolData as hs
import numpy as np
import re
import matplotlib.pyplot as plt
import seaborn as sns


filter_cols= ["school_name","borocode", "language_classes",
"advancedplacement_courses","location","subway","bus",
"total_students","start_time","end_time","psal_sports_boys","psal_sports_girls","psal_sports_coed",
"graduation_rate","attendance_rate","college_career_rate"]
# takes a year btwn 2017 and 2021 to analyze
# returns a dictionary that maps each borough symbol to a df
def analyzeHighschool(year)-> dict:
  offset= 35
  if(int(year)<2017 or int(year)>2021):
    print('-'* offset)
    print('- No data found for year', year)
    print('- REASON :')
    print('-', year, 'is not between 2017 - 2021')
    print('-'* offset)
    quit()
  file_name='data/0000_DOE_High_School_Directory.csv'
  file_name= file_name.replace('0000',str(year))
  highschool= hs.createDataFrame(file_name)
  st=file_name[5:9]
  print('-'* (offset//2),st,'-'* (offset//2),'\n\n')
  
  return hs.createDataFrame(file_name)
# hs2020= analyzeHighschool(2020)
# m2020= hs.schoolBoro(hs2020,'brooklyn')
# print(m2020)
# print(m2020['bus'])
# print(m2020['subway'])
# print(hs.avgBusRoutes(m2020))
# print(hs.popularBusRoutes(m2020))
# print(hs.getSubwayFreq(m2020))


def analyzeCovid()-> pd.DataFrame:
  file_name= 'data\COVID-19_Daily_Counts_of_Cases__Hospitalizations__and_Deaths.csv'
  df = pd.read_csv(file_name)
  return df

def graphCovid(df)-> None:
  df['days']=pd.to_datetime(df['DATE_OF_INTEREST'])
  
  startingDate= df['days'].iloc[0]
  df['days']=(df['days']-startingDate).dt.days

  sns.lmplot(x='days', y='CASE_COUNT', data= df, fit_reg=False)
  plt.title('Historical Covid Data')
  plt.show()

  return


# pd.set_option('display.max_columns',None)
# pd.set_option('display.max_rows',None)

covid2020 =analyzeCovid()
graphCovid(covid2020)