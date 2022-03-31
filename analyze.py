from numpy import extract
import pandas as pd
import covidData as Covid
import highschoolData as hs
import json

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

hs2020= analyzeHighschool(2020)
m2020= hs.schoolBoro(hs2020,'brooklyn')
# print(m2020)
# print(m2020['bus'])
# print(m2020['subway'])
# print(hs.avgBusRoutes(m2020))
# print(hs.popularBusRoutes(m2020))
# print(hs.getSubwayFreq(m2020))
text ='2, 3, 4, 5 to Borough Hall; A, C, F, R to Jay St-MetroTech; B, Q to DeKalb Ave; G to Hoyt & Schermerhorn'
print(hs.extractTrains(text))