"""_summary_
compares cases with boro attendance on a scatter plot. saves graphs as png image
"""

import pandas as pd
from attendance import AttendanceDf
from covidData import *
from statModels import *
from cleanDate import *
from boroughs import *
import numpy as np

# merge the covid and cases dataframe
AttendanceDf= AttendanceDf.drop(columns=['Month'])
monthlyCases= cleanDate(monthlyData(covidCases))
AvC= pd.merge(AttendanceDf,monthlyCases, how= 'outer', on ='Date')

# impute missing values
AvC= AvC.fillna(0).sort_values(by='Date').reset_index(drop=True)
# collective covid and avg attendance cases per month

import seaborn as sns
import matplotlib.pyplot as plt


# to make dataframe easier to work with
# we'll create a borough category
# manually place each borough's data as a row entry
covidAttendance= pd.DataFrame()

for b in boroList:
  att = (AvC[f'{b} Attendance%']).tolist()
  dates= (AvC['Date']).tolist()
  covidCases= (AvC[b]).tolist()
  
  for i in range(len(att)):
    row=pd.DataFrame({
      'Borough': b,
      'Attendance%': att[i],
      'Date':dates[i],
      'Cases':covidCases[i]
    },index= [0])
    covidAttendance = pd.concat([covidAttendance,row])
covidAttendance= covidAttendance.reset_index(drop= True)
  
# Attendance Timeline
covidAttendance= covidAttendance.dropna()
covidAttendance= covidAttendance.loc[covidAttendance['Attendance%']!=0].reset_index(drop=True)

plt.figure()
Att= sns.scatterplot(
  data= covidAttendance,
  x= 'Date',
  y= 'Attendance%',
  hue= 'Borough'
)
Att.set(
  ylim=(70, 100),
)
Att.set_xlabel('Date', fontsize=20)
Att.set_ylabel('Attendance Rates', fontsize=20)
plt.legend()
plt.xticks(rotation = 45)
plt.savefig(
  f"graphs/AttendanceTimeline.png",
  bbox_inches="tight",
  dpi=300,
  transparent=True
)
# plt.show()
plt.close()

# # covid vs attendance rate scatterplot
# def covidScatter(covidDf,extraText:str= "withPrev"):
#   for order in range (1,9):
#     file_name= f'graphs/poly/covidAttendanceAll{extraText}order{order}.png'
#     createPolyReg(covidDf,'Cases','Attendance%',file_name,order)
  
#   # plot each borough
#   for b in boroList:
#     boroData= covidDf.loc[covidDf['Borough']==b]
#     for order in range (1,9):
#       file_name=f'graphs/poly/covidAttendance{b}{extraText}order{order}.png'
#       createPolyReg(boroData,'Cases','Attendance%',file_name, order, boroColor[b])

# # # scatter attendance based on covid
# # covidScatter(covidAttendance)

# # # scatter attendance based on covid (exclude where cases==0)
# # covidDf= covidAttendance.loc[covidAttendance['Cases']!=0]
# # covidScatter(covidDf, "")