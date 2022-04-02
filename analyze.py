"""
Resources:
https://stackoverflow.com/questions/42128467/matplotlib-plot-multiple-columns-of-pandas-data-frame-on-the-bar-chart
https://stackoverflow.com/questions/43214978/seaborn-barplot-displaying-values
https://stackoverflow.com/questions/33227473/how-to-set-the-range-of-y-axis-for-a-seaborn-boxplot
https://stackabuse.com/rotate-axis-labels-in-matplotlib/

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

def highschoolGraph(df,boro):
  graph= df.plot(x='year',y=boro, kind= 'bar', width= .7)
  graph.bar_label(graph.containers[0])
  graph.bar_label(graph.containers[1])
  graph.bar_label(graph.containers[2])
  graph.bar_label(graph.containers[3])
  graph.bar_label(graph.containers[4])
  plt.ylim(.65,1)
  plt.title('Highschool Graduation Rates by Borough')
  graph.tick_params(axis='x', labelrotation = 0)
  return graph

def CovidDF()-> pd.DataFrame:
  file_name= 'data\COVID-19_Daily_Counts_of_Cases__Hospitalizations__and_Deaths.csv'
  df = pd.read_csv(file_name)
  return df

def covidGraph(df,boros)-> None:
  # df['days']=pd.to_datetime(df['school_year'])
  # startingDate= df['days'].iloc[0]
  # df['days']=(df['days']-startingDate).dt.days

  graph= df.plot(x='school_year', y=boros, kind= 'bar')
  plt.title('Historical Covid Data')
  return graph

# pd.set_option('display.max_columns',None)
# pd.set_option('display.max_rows',None)

hsGradRates= highschoolGraph(hs.graduationDf(), boroughs.boros)

covidCases= (Covid.covidSummaryDF())
covidplot = covidGraph(covidCases, boroughs.boros)


plt.show()