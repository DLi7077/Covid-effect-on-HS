"""
Resources:
https://stackoverflow.com/questions/42128467/matplotlib-plot-multiple-columns-of-pandas-data-frame-on-the-bar-chart
https://stackoverflow.com/questions/43214978/seaborn-barplot-displaying-values
https://stackoverflow.com/questions/33227473/how-to-set-the-range-of-y-axis-for-a-seaborn-boxplot
https://stackabuse.com/rotate-axis-labels-in-matplotlib/
https://www.pythontutorial.net/python-basics/python-filter-list/
https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.merge.html
"""

import pandas as pd
import covidData as Covid
import highschoolData as hs
import numpy as np
import re
import matplotlib.pyplot as plt
import seaborn as sns
import boroughs


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
  
  return hs.createDataFrame(year)
# hs2020= analyzeHighschool(2020)
# m2020= hs.schoolBoro(hs2020,'brooklyn')
# print(m2020)
# print(m2020['bus'])
# print(m2020['subway'])
# print(hs.avgBusRoutes(m2020))
# print(hs.popularBusRoutes(m2020))
# print(hs.getSubwayFreq(m2020))

def highschoolGraph(df,boros):
  # filter only boroughs
  boros= list(filter(lambda b: b in boroughs.boros, boros))
  graph= df.plot(x='year',y=boros, kind= 'bar', width= .7)
  graph.bar_label(graph.containers[0])
  plt.ylim(.65,1)
  title= boros[0].title() if len(boros)==1 else "All Boroughs"
  plt.title(f'{title}: Highschool Graduation Rates')
  plt.legend(loc='upper left')
  graph.tick_params(axis='x', labelrotation = 0)
  return graph

def CovidDF()-> pd.DataFrame:
  file_name= 'data\COVID-19_Daily_Counts_of_Cases__Hospitalizations__and_Deaths.csv'
  df = pd.read_csv(file_name) 
  return df

def covidGraph(df,boros)-> None:
  # filter only boroughs
  boros= list(filter(lambda b: b in boroughs.boros, boros))
  title= boros[0].title() if len(boros)==1 else "All Boroughs"
  graph= df.plot(x='school_year', y=boros, kind= 'line')
  plt.ylim(0,400000)
  plt.legend(loc='upper left')
  plt.title(f'{title}: New Covid Cases by School Year')
  return graph

# pd.set_option('display.max_columns',None)
# pd.set_option('display.max_rows',None)

# provided covidDF and graduationDF, return a df such that:
# the df shall contain cols: ['school_year','case_count','graduation_rate']
# params: covidDF-> contains ['school_year','case_count',...boros]
#         graduationDF->     ['year','graduation_rate',...boros]

def mergeData(covidDF: pd.DataFrame, graduationDF: pd.DataFrame)-> pd.DataFrame:
  # confirm parameters are in right order
  if ('school_year' not in covidDF.columns):
    print("first parameter doesn't have school_year as column")
    quit()
  df= pd.merge(covidDF, graduationDF,
               left_on= 'school_year',
               right_on='year')
  df= df.dropna()
  return df

def filterBoroughs(df:pd.DataFrame,boro: str)-> pd.DataFrame:
  cols=['school_year']
  for colName in df.columns:
    if(boro in colName):
      cols.append(colName)
  return df[cols]

# plot data for each borough 
covidCases= Covid.covidSummaryDF()
highschoolGradDF=hs.graduationDf()

merged= mergeData(covidCases,highschoolGradDF)
# for b in boroughs.boros:
#   hsGradplot= highschoolGraph(highschoolGradDF, [b])
#   covidplot = covidGraph(covidCases, [b])
#   plt.show()

# scatterplot
# plots covid_cases as X and graduation rate as y
for boro in boroughs.boros:
  filtered= filterBoroughs(merged,boro)
  covid_x= sns.scatterplot(x=boro+'_x', y=boro+'_y', data=filtered)
  covid_x.set(ylim=(.6,1))
  
  year_x= sns.scatterplot(x='school_year', y=boro+'_y', data=filtered)
  
  plt.show()

