"""
Resources:
accessing groupby object
https://stackoverflow.com/questions/14734533/how-to-access-pandas-groupby-dataframe-by-key
groupby month and year
https://stackoverflow.com/questions/26646191/pandas-groupby-month-and-year
"""
import pandas as pd
from boroughs import boros as boroList
def createDataFrame()-> pd.DataFrame:
    df =pd.read_csv('attendance/2018-2021_Daily_Attendance_by_School.csv')
    df['Date'] =pd.to_datetime(df['Date'])
    # identifies school borough based on school DBN
    # DBN will be 6 digits, where the 3rd character is the boroCode
    def schoolDist(DBN:str)->str:
        # boroMap= {
        # 'X':'Bronx',
        # 'K':'Brooklyn',
        # 'R':'Staten island',
        # 'M':'Manhattan',
        # 'Q':'Queens'
        # }
        return [DBN[:2]]
    df['District']= df['School DBN'].apply(schoolDist)
    
    df= df.drop(columns=['School DBN','SchoolYear'])
    
    # df= df.groupby(['Date','Borough']).sum()
    # df= df.groupby([(df['Date'].dt.year),df['Date'].dt.month,'Borough']).sum()
    def addExtraFiles(file_name):
        newDF= pd.read_csv(file_name)
        newDF= newDF.drop()
        pd.concat(df,newDF)
        return
    
    df['Attendance'] = round((df['Present']/(df['Present']+df['Absent']+df['Released'])),5)
    df= df.drop(columns= ['Enrolled','Present','Absent','Released'])
    df.sort_values(by=['Date'])
    
    return df

def getSchoolDistrict(df, district:str)->pd.DataFrame:
    dist= (district.lower()).title()
    # if(dist not in boroList):
    #     print(f'{district} not in boroList')
    #     print(f'valid boroughs: {boroList}')
    #     quit()
    filtered= df.loc[df['District']==dist]
    filtered['Month'] = filtered['Date'].dt.month
    filtered['Year'] = filtered['Date'].dt.year
    filtered= filtered.drop(columns=['Date','District'])
    filtered= filtered.groupby(['Year','Month']).mean()
    filtered= filtered.reset_index()
    
    return filtered

def create(file_name):
    df =pd.read_csv(file_name)
    

pd.set_option('display.max_rows',None)
p=createDataFrame()
# p=getSchoolDistrict(p,'34')
print(p)