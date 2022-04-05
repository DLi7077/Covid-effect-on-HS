import pandas as pd

def createDataFrame()-> pd.DataFrame:
    df =pd.read_csv('attendance/2018-2021_Daily_Attendance_by_School.csv')
    df['Date'] =pd.to_datetime(df['Date'])

    # identifies school borough based on school DBN
    # DBN will be 6 digits, where the 3rd character is the boroCode
    def schoolBoro(DBN:str)->str:
        boroMap= {
        'X':'Bronx',
        'K':'Brooklyn',
        'R':'Staten island',
        'M':'Manhattan',
        'Q':'Queens'
        }
        return boroMap[DBN[2]]
    df['boro']= df['School DBN'].apply(schoolBoro)
    attendanceDF= pd.DataFrame()
    attendanceDF['boro']= df['boro']
    attendanceDF['Present']= df['Present']
    attendanceDF['Absent']=df['Absent']
    attendanceDF= attendanceDF.groupby('boro').sum()
    
    attendanceDF['Rate'] = attendanceDF['Present']/(attendanceDF['Absent']+attendanceDF['Present'])
    return attendanceDF

p=createDataFrame()
print(p)