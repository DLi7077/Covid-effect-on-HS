from attendance import schoolAttendanceDf as attendanceDF
from covidData import boroData, casesDF,hospitalDF,deathDF
from boroughs import boroughList
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

attendanceDF # historical school attendance
def convertToDays(DT):
  startingMonth= 9
  currMonth= DT.month
  currYear= (DT.year - 2018)* 12
  
  return currYear+ currMonth-startingMonth

attendanceDF['Months']= pd.to_datetime(attendanceDF['Date']).apply(convertToDays)


monthSet= set(np.arange(38))
# append missing months
prevMonth =-1
for i,row in attendanceDF['Months'].iteritems():
  if(row in monthSet):
    monthSet.remove(row)

print(monthSet)

from pandas.tseries.offsets import MonthEnd
# to add the missing months
for m in monthSet:
  i =0
  for b in boroughList:
    actualMonth= (m+9)%12
    if(actualMonth==0): actualMonth= 12
    actualYear= 2018+(m+9)//12
    tempRow= pd.DataFrame({
      'Borough': b,
      'Attendance%': 0,
      'Date': pd.to_datetime(f'{actualYear}-{actualMonth}', format= '%Y-%m')+MonthEnd(1),
      'Months': m
    }, index=[m+i])
    i+=1
    # print(tempRow)
    attendanceDF= pd.concat([attendanceDF, tempRow])
attendanceDF= attendanceDF.sort_values(by= ['Months','Date'])


pd.options.display.max_rows= None
print(attendanceDF)

# merge covid graph with highschool graph.
# first, reshape the covid graph
# print(casesDF)

boros= list(filter(lambda b: b in boroughList, boroughList))

def attendanceLine():
  plt.figure('Attendance')
  # filter for boroughs
  for b in boros:
    df= attendanceDF.loc[attendanceDF['Borough']==b]
    timeline =df['Date'].tolist()
    attendance= np.array(df['Attendance%'].tolist())
    attendance[attendance==0]= np.nan
    
    plt.plot(timeline, attendance, label =b)
  # plt.title = title
  plt.xticks(rotation = 45)
  plt.legend()
  plt.ylim((75,100))

def AttendanceScatter():
  plt.figure('Scatterplot')
  for b in boros:
    df= attendanceDF.loc[attendanceDF['Borough']==b]
    timeline =df['Date'].tolist()
    attendance= np.array(df['Attendance%'].tolist())
    attendance[attendance==0]= np.nan
    
    plt.scatter(timeline, attendance, label =b)
  # plt.title = title
  plt.xticks(rotation = 45)
  plt.legend()
  plt.ylim((75,100))

attendanceLine()

AttendanceScatter()

plt.show()