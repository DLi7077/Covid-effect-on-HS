import pandas as pd
import os

for filename in os.listdir("new attendance"):
  with open(os.path.join("new attendance", filename), 'r') as f:
    df= pd.read_csv(f)
    print(f'file date: {filename[:-4]}')
    # filter for only highschools
    

    df= df.rename(columns={
      'SCHOOL': 'school_code',
      'SCHOOL NAME': 'school_name',
      'ATTD DATE': 'Date',
      '%ATTD': 'attendance_rate'
    })
    
    def isHighschool(schoolName:str)->bool:
      schoolName =schoolName.lower()
      return ('high school' in schoolName)
    
    df= df.loc[df['school_name'].apply(isHighschool)].reset_index(drop=True)
    
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
    
    df['Date'] = pd.to_datetime(df['Date'])
    
    print(df)
    