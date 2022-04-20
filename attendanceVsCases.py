import pandas as pd
from attendance import AttendanceDf
from covidData import casesDF

# merge the covid and cases dataframe
AttendanceDf= AttendanceDf.drop(columns=['Month'])
AvC= pd.merge(AttendanceDf,casesDF, how= 'outer', on ='Date')
AvC= AvC.fillna(0)
print(AvC)