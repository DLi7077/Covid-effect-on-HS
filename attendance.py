"""
Resources:
accessing groupby object
https://stackoverflow.com/questions/14734533/how-to-access-pandas-groupby-dataframe-by-key
groupby month and year
https://stackoverflow.com/questions/26646191/pandas-groupby-month-and-year
to_numeric
https://pandas.pydata.org/docs/reference/api/pandas.to_numeric.html
"""

import pandas as pd
from boroughs import *
import re
import numpy as np

def keyToBoro(boro:str)->str:
    boroMap= {
    'X':'Bronx',
    'K':'Brooklyn',
    'R':'Staten Island',
    'M':'Manhattan',
    'Q':'Queens'
    }
    return boroMap[boro[2]]

# mass attendance data from 2018-part of 2020
def createAttendanceDataFrame()-> pd.DataFrame:
    df =pd.read_csv('attendance/2018-2021_Daily_Attendance_by_School.csv')
    df['Date'] =pd.to_datetime(df['Date'])
    # identifies school borough based on school DBN
    # DBN will be 6 digits, where the 3rd character is the boroCode

    df['Borough']= df['School DBN'].apply(keyToBoro)
    df= df.drop(columns=['School DBN','SchoolYear'])
    df['Year']= df['Date'].dt.year
    df['Month'] =df['Date'].dt.month
    df= df.groupby(['Year','Month','Borough']).sum()
    df['Attendance%'] = 100*(df['Present']/(df['Present']+df['Absent']+df['Released']))
    df= df.drop(columns= ['Enrolled','Present','Absent','Released'])
    return df.reset_index()

# attendance from 2021 (remote learning), but the data is clean
# returns a df Row, containing each boro's average attendance for that month
def data2021(df):
    df= df.rename(columns={'Overall Attendance Rate':'Attendance%'})
    df['Borough'] =df['DBN'].apply(keyToBoro)
    df= df[['Borough','Attendance%']]
    df= df.groupby('Borough').mean()
    return df.reset_index()

# attendance from 2021 (remote learning), but the data has unneeded categories
# returns a df Row, containing each boro's average attendance for that month
def ugly2021(df):
    df= df[['Geographic Unit','Student Category 1','Overall Attendance Rate']]
    df= df.rename(columns={'Overall Attendance Rate':'Attendance%'})
    # some values are labeled s
    df= df.loc[df['Attendance%']!='s']
    df['Attendance%']=df['Attendance%'].astype('float64')

    # target highschool students
    highschoolStudents= ['Grade 09','Grade 10','Grade 11','Grade 12']
    df= df.loc[df['Student Category 1'].isin(highschoolStudents)]
    # target schools in valid districts
    
    
    # if the value has district in name, then it's a district
    def isDistrict(unit:str):
        return 'District' in unit
    df= df.loc[df['Geographic Unit'].apply(isDistrict)]
    df= df[['Geographic Unit', 'Attendance%']]

    # helper function to convert district to borough
    # https://data.nysed.gov/profile.php?instid=7889678368
    def districtBorough(num: int):
        id = int(num[9:])
        districtMap= {
            1 : 'Manhattan',
            2 : 'Manhattan',
            3 : 'Manhattan',
            4 : 'Manhattan',
            5 : 'Manhattan',
            6 : 'Manhattan',
            7 : 'Bronx',
            8 : 'Bronx',
            9 : 'Bronx',
            10 : 'Bronx',
            11 : 'Bronx',
            12 : 'Bronx',
            13 : 'Brooklyn',
            14 : 'Brooklyn',
            15 : 'Brooklyn',
            16 : 'Brooklyn',
            17 : 'Brooklyn',
            18 : 'Brooklyn',
            19 : 'Brooklyn',
            20 : 'Brooklyn',
            21 : 'Brooklyn',
            22 : 'Brooklyn',
            23 : 'Brooklyn',
            24 : 'Queens',
            25 : 'Queens',
            26 : 'Queens',
            27 : 'Queens',
            28 : 'Queens',
            29 : 'Queens',
            30 : 'Queens',
            31 : 'Staten Island',
            32 : 'Brooklyn',
            75 : 'idk',
            79 : 'idk'
        }
        return districtMap[id]
    # translate district to boroughs
    df['Borough'] = df['Geographic Unit'].apply(districtBorough)
    # choose boroughs with valid matching
    df= df.loc[df['Borough']!='idk']
    df.rename(columns={'Geographic Unit':'Borough'})

    # merge borough attendance rates
    df= df.groupby('Borough').mean()
    df= df.reset_index()

    return df

# create dataframes and merge them
# Base Empty Dataframe:
baseDF= createAttendanceDataFrame()

# extra months files that we can add for 2021:
monthList = {'01','02','03','04','05','09','10'}

# append the extra months
for month in monthList:
    file_name= f'attendance/{month}_2021.csv'
    df = pd.read_csv(file_name)
    if('DBN' in df.columns): # file isnt ugly, read normally
        df = data2021(df)
    else:
        df= ugly2021(df)

    # figure out the date from the month
    regex= r'/.+\.'
    date= (re.findall(regex,file_name)[0][1:-1]).split('_')
    df['Year']= int(date[1])
    df['Month']= int(date[0])

    # add the extra data
    baseDF= pd.concat([baseDF,df])

# rearrange the dataframe
# new cols will be [boro0,boro1,boro2,... date, months]
# let 'Months' col represent the amount of months since Sept 2018
baseDF['Months']= (baseDF['Month']-9 + 12*(baseDF['Year'] -2018))

# now to make Month and Year plottable:
# we'll convert it to a datetime using a helper function
from pandas.tseries.offsets import MonthEnd # for end of month date
def cleanDate(df):
    copy= df
    dateSeries= pd.to_datetime(
        df[['Year','Month']].assign(DAY=1)
    )
    df['Date']= pd.to_datetime(
        dateSeries,format='%Y%m'
        ) +MonthEnd(1)
    
    return df.drop(columns = ['Year','Month'])
    
baseDF= cleanDate(baseDF)
baseDF= baseDF.sort_values(by=['Months','Borough'])

AttendanceDf= pd.DataFrame()

# for all rows in baseDF, spread it out to 1 row
for idx in range(0,len(baseDF),5):
    rowEntry= baseDF.iloc[idx:idx+5].reset_index()
    cols = rowEntry['Borough'].tolist()
    attendance= rowEntry['Attendance%'].tolist()

    newRow= {}
    
    for i in range(len(cols)):
        newRow[f'{cols[i]} Attendance%']= attendance[i]

    newRow['Month']= baseDF.iloc[idx,2]
    newRow['Date'] =baseDF.iloc[idx,3]
    newRow= pd.DataFrame(newRow,index=[idx])

    AttendanceDf=pd.concat([AttendanceDf,newRow])

AttendanceDf=AttendanceDf.reset_index(drop=True)

# problem: some dates are left out bc of summer/ breaks
# manually add the months and set the attendance to be 0

monthSet= set(np.arange(38))

# removing existing months
for i,row in AttendanceDf['Month'].iteritems():
  if(row in monthSet):
    monthSet.remove(row)

# add each missing month
print(monthSet)
for m in monthSet:
  newRow = {}
  for b in boroSet:
    newRow[f'{b} Attendance%']=0
  newRow['Month']=m
  
  # we start at september, so consider +9 to calculation
  actualMonth= (m+9)%12
  if(actualMonth==0):
    actualMonth= 12
  actualYear= 2018+(m+9)//12
  newRow['Date']= pd.to_datetime(f'{actualYear}-{actualMonth}', format= '%Y-%m')+MonthEnd(1)
  newRow= pd.DataFrame(newRow, index= [0])
  AttendanceDf= pd.concat([AttendanceDf,newRow])

AttendanceDF= AttendanceDf.sort_values(by= ['Month','Date']).reset_index(drop=True)
print(AttendanceDF)
# finally done. Data is cleaned and now  we have each borough's avg attendance rate per month
# Unfortunately, this is only from 2018- to Oct 2021, with a missing chunk in 2020 due to attendance not being taken during covid

import seaborn as sns
import matplotlib.pyplot as plt
timeline = AttendanceDF['Date'].tolist()
for b in boroList:
  boroRates= AttendanceDF[f'{b} Attendance%'].tolist()
  boroRates= np.array(boroRates, dtype=np.double)
  boroRates[boroRates==0] = np.nan
  print(boroRates)
  sns.scatterplot(
		x=timeline,
		y=boroRates
	)
plt.show()