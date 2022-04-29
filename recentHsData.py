from numpy import cov
import pandas as pd
import os

# Plan: Using recent data as a sample:
# Calculate the mean attendance rate
# Compare with historical monthly pattern

recentHsData = pd.DataFrame()
# list of highSchools. We need this bc they also slapped in middle school attendance
file = pd.read_csv('data/2017_DOE_High_School_Directory.csv')

def lowercase(schoolName:str)->str:
  return schoolName.lower()

highSchoolList= set(file['school_name'].apply(lowercase).tolist())

for filename in os.listdir("new attendance"):
  with open(os.path.join("new attendance", filename), 'r') as f:
    df= pd.read_csv(f)
    df= df.rename(columns={
      'SCHOOL': 'school_code',
      'SCHOOL NAME': 'school_name',
      'ATTD DATE': 'Date',
      '%ATTD': 'attendance_rate'
    })
     
    # remove non numeric rows in col
    # https://stackoverflow.com/questions/33961028/remove-non-numeric-rows-in-one-column-with-pandas
    df =df[pd.to_numeric(df['attendance_rate'], errors='coerce').notnull()]
    
    # to_numeric
    # https://stackoverflow.com/questions/15891038/change-column-type-in-pandas
    df['attendance_rate'] = pd.to_numeric(df['attendance_rate'])
    
    # filter for only highschools
    def isHighschool(schoolName:str)->bool:
      schoolName = schoolName.lower()
      for highschool in highSchoolList:
        if(schoolName in highschool or highschool in schoolName):
          return True
      return False
    
    df= df.loc[df['school_name'].apply(isHighschool)].reset_index(drop=True)
    
    # get borough of the school
    def keyToBoro(schoolCode:str)->str:
      boroMap= {
      'X':'Bronx',
      'K':'Brooklyn',
      'R':'Staten Island',
      'M':'Manhattan',
      'Q':'Queens'
      }
      return boroMap[schoolCode[2]]
    
    df['Borough'] = df['school_code'].apply(keyToBoro)
    
    # we know the date will be the month of april
    df = df.drop(columns=['school_code','Date']) 
    recentHsData= pd.concat([recentHsData,df]).reset_index(drop=True)
    
    
# https://stackoverflow.com/questions/29583312/pandas-sum-of-duplicate-attributes

# aggregate average attendance for sample 
recentHsData['attendance_rate'] = recentHsData.groupby(
  ['school_name','Borough']
)['attendance_rate'].transform('mean')

# remove dupes
recentHsData = recentHsData.drop_duplicates(subset=['school_name'])
recentHsData = recentHsData.sort_values(by='school_name').reset_index(drop=True)
from covidData import *

# clean up data for april of 2022
cases = caseDF.loc[(caseDF['Date'].dt.month==4)&(caseDF['Date'].dt.year==2022)].drop(columns=['Date'])
cases= cases.groupby('Borough')['Cases'].sum().reset_index()
cases['Date'] = pd.to_datetime('4-30-2022')

# merge data with april's covid data 
recentHsData = recentHsData.merge(right = cases, on = 'Borough')
recentHsData = recentHsData.rename(columns={
  'attendance_rate': 'Attendance%'
})
from statModels import *
from boroughs import *
from attendanceVsCases import *
# compare to previous data (all boroughs)
# plot previous data (from attendance vs Covid)


def plotComparison(covidAttendance,recentHsData,xCol='Cases', yCol='Attendance%', prev=""):
  Past= covidAttendance
  Data= recentHsData
  plt.figure()
  sns.regplot(
    data=Past,
    x=xCol,
    y=yCol,
    x_jitter=200,
    scatter_kws={'alpha':0.3}
  )

  sns.regplot(
    data=Data,
    x=xCol,
    y=yCol,
    x_jitter=100,
    scatter_kws={'alpha':0.069}
  )
  avgAttendace = Data[yCol].mean()
  cases = Data[xCol].mean()

  slope, intercept = computeLinearReg(Past, xCol, yCol)
  expectedAtten = cases*slope + intercept
  plt.text(
    20000,60,
    f'Correlation: {round(Past[xCol].corr(Past[yCol]),2)}'+
    f'\nLinear Line:\nSlope: {round(slope,4)}\nY-Intercept: {round(intercept,4)}'+
    f'\nExpected Attendance: {round(expectedAtten,2)}'+
    f'\nActual Attendance: {round(avgAttendace,2)}({round(avgAttendace-expectedAtten,2)})'
  )
  plt.plot(cases,avgAttendace, marker="o", markersize=10, color = 'black')
  plt.ylim(50,100)
  plt.xlim(-1000,50000)
  # plt.savefig(
  #   f'graphs/poly/extrapolate/All{prev}order1',
  #   bbox_inches="tight",
  #   dpi=300,
  #   transparent=True
  # )
  # plt.show()
  plt.close()

  # compare current data to preivous data (BOROUGHS)
  for b in boroList:
    plt.figure()
    # plot previous data (from attendance vs Covid)
    BoroPast= covidAttendance.loc[covidAttendance['Borough']==b]
    boroData= recentHsData.loc[recentHsData['Borough']==b]
    boroData =boroData.rename(columns={
      'attendance_rate': 'Attendance%'
    })
    
    sns.regplot(
      data=BoroPast,
      x='Cases',
      y='Attendance%',
      x_jitter=100,
      color =boroColor[b],
      scatter_kws={'alpha':0.5}
    )
    slope, intercept = computeLinearReg(BoroPast, 'Cases', 'Attendance%')

    sns.regplot(
      data=boroData,
      x='Cases',
      y='Attendance%',
      x_jitter=100,
      color =boroColor[b],
      scatter_kws={'alpha':0.069}
    )
    avgAttendace = boroData['Attendance%'].mean()
    cases = boroData['Cases'].mean()
    expectedAtten = cases*slope + intercept
    plt.text(
      20000,60,
      f'Correlation: {round(BoroPast[xCol].corr(BoroPast[yCol]),2)}'+
      f'\nLinear Line:\nSlope: {round(slope,4)}\nY-Intercept: {round(intercept,4)}'+
      f'\nExpected Attendance: {round(expectedAtten,2)}'+
      f'\nActual Attendance: {round(avgAttendace,2)}({round(avgAttendace-expectedAtten,2)})'
    )
    plt.plot(cases,avgAttendace, marker="o", markersize=10, color = 'black')
    plt.ylim(50,100)
    plt.xlim(-1000,50000)
    # plt.savefig(
    #   f'graphs/poly/extrapolate/{b}{prev}order1',
    #   bbox_inches="tight",
    #   dpi=300,
    #   transparent=True
    # )
    # plt.show()
    plt.close()

plotComparison(covidAttendance, recentHsData,'Cases','Attendance%',prev='withPrev')
noCases = covidAttendance.loc[covidAttendance['Cases']!=0]
plotComparison(noCases, recentHsData,'Cases','Attendance%')