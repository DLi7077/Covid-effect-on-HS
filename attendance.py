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
from pyparsing import col
from boroughs import boroughList as boroList
import re

def schoolBoro(boro:str)->str:
    boroMap= {
    'X':'Bronx',
    'K':'Brooklyn',
    'R':'Staten Island',
    'M':'Manhattan',
    'Q':'Queens'
    }
    return boroMap[boro[2]]

def createDataFrame()-> pd.DataFrame:
    df =pd.read_csv('attendance/2018-2021_Daily_Attendance_by_School.csv')
    df['Date'] =pd.to_datetime(df['Date'])
    # identifies school borough based on school DBN
    # DBN will be 6 digits, where the 3rd character is the boroCode

    df['Borough']= df['School DBN'].apply(schoolBoro)
    
    df= df.drop(columns=['School DBN','SchoolYear'])
    
    df['Year']= df['Date'].dt.year
    df['Month'] =df['Date'].dt.month
    df= df.groupby(['Year','Month','Borough']).sum()
    df['Attendance%'] = 100*(df['Present']/(df['Present']+df['Absent']+df['Released']))
    df= df.drop(columns= ['Enrolled','Present','Absent','Released'])
    return df.reset_index()
# district to borough
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

def data2021(df):
    
    df= df.rename(columns={'Overall Attendance Rate':'Attendance%'})
    df['Borough'] =df['DBN'].apply(schoolBoro)
    df= df[['Borough','Attendance%']]
    df= df.groupby('Borough').mean()
    
    return df.reset_index()

def isDistrict(unit:str):
    return 'District' in unit

def ugly2021(df):
    # read file
    # modify columns
    df= df[['Geographic Unit','Student Category 1','Overall Attendance Rate']]
    df= df.rename(columns={'Overall Attendance Rate':'Attendance%'})
    
    df= df.loc[df['Attendance%']!='s']  
    
    df['Attendance%']=df['Attendance%'].astype('float64')
    
    # target districts
    # target highschool students
    highschoolStudents= ['Grade 09','Grade 10','Grade 11','Grade 12']
    
    df= df.loc[df['Student Category 1'].isin(highschoolStudents)]
    df= df.loc[df['Geographic Unit'].apply(isDistrict)]
    df= df[['Geographic Unit', 'Attendance%']]
    
    # translate district to boroughs
    df['Borough'] = df['Geographic Unit'].apply(districtBorough)
    df= df.loc[df['Borough']!='idk']
    df= df.drop(columns='Geographic Unit')

    # merge boroughs
    df= df.groupby('Borough').mean()
    df= df.reset_index()
    
    # done
    return df


# TODO: create a function that loops through all the data
# and combines it to 1 dataframe, one for each borough
# graph the results
# consider the impact and implications



# create dataframes and merge them
# first big dataframe:
schoolAttendanceDf= createDataFrame()


# create other monthly dataframes:
monthList = ['01','02','03','04','05','09','10']

# append the extra months
for month in monthList:
    file_name= f'attendance/{month}_2021.csv'
    df = pd.read_csv(file_name)
    if('DBN' in df.columns):
        df = data2021(df)
    else:
        df= ugly2021(df)
        
    # figure out the date
    regex= r'/.+\.'
    date= (re.findall(regex,file_name)[0][1:-1]).split('_')
    df['Year']= int(date[1])
    df['Month']= int(date[0])
    
    # add the extra data
    schoolAttendanceDf= pd.concat([schoolAttendanceDf,df])

#

from cleanDate import cleanDate

schoolAttendanceDf= cleanDate(schoolAttendanceDf)
