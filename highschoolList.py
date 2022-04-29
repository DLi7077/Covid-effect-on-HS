import pandas as pd
file = pd.read_csv('data/2017_DOE_High_School_Directory.csv')

def lowercase(schoolName:str)->str:
  return schoolName.lower()

highSchoolList= set(file['school_name'].apply(lowercase).tolist())
# print(highSchoolList)