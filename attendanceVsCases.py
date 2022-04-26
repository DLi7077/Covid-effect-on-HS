"""_summary_
compares cases with boro attendance on a scatter plot. saves graphs as png image
"""

import pandas as pd
from attendance import AttendanceDf
from covidData import *
from statModels import computeLinearReg
from cleanDate import *
from boroughs import *
import numpy as np

# merge the covid and cases dataframe
AttendanceDf= AttendanceDf.drop(columns=['Month'])
monthlyCases= cleanDate(monthlyData(covidCases))
# print(monthlyCases)
AvC= pd.merge(AttendanceDf,monthlyCases, how= 'outer', on ='Date')

# impute missing values
AvC= AvC.fillna(0).sort_values(by='Date').reset_index(drop=True)
print(AvC)
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
covidAttendance= covidAttendance.loc[covidAttendance['Attendance%']!=0]
print(covidAttendance)

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
plt.savefig(
  f"graphs/AttendanceTimeline.png",
  bbox_inches="tight",
  dpi=300,
  transparent=True
)
# plt.show()
plt.close()

# covid vs attendance rate scatterplot
def covidScatter(covidDf,extraText:str= "withPrev"):
  # plot data for all boroughs
  plt.figure()
  cases= sns.scatterplot(
    data= covidDf,
    x='Cases',
    y='Attendance%',
    hue= 'Borough'
  )
  cases.set(
    xlim=(-1000,45000),
    ylim=(50, 100),
  )
  plt.legend(loc='lower left')
  slope, intercept = computeLinearReg(covidDf,'Cases','Attendance%')

  xVals= np.array(range(-1000,45000))
  transform= lambda x: x*slope +intercept
  yVals= transform(xVals)
  plt.plot(xVals,yVals)
  plt.text(
    30000,60,
    f'Slope: {round(slope,4)}\nY-Intercept: {round(intercept,4)}'
  )
  plt.title( f"All Boroughs\nr= {round(covidDf['Cases'].corr(covidDf['Attendance%']),4)}")
  plt.savefig(
    f"graphs/covidAttendanceAll{extraText}.png",
    bbox_inches="tight",
    dpi=300,
    transparent=True
  )
  # plt.show()
  plt.close()
  
  # plot each borough
  for b in boroList:
    plt.figure()
    boroData= covidDf.loc[covidDf['Borough']==b]
    cases= sns.regplot(
      data= boroData,
      x='Cases',
      y='Attendance%',
      color=boroColor[b],
      x_jitter=500,
      scatter_kws={'alpha':0.5}
    )
    cases.set(
    xlim= (-1000, 45000),
    ylim=(50, 100),
    )
    slope, intercept = computeLinearReg(boroData,'Cases','Attendance%')
    
    xVals= np.array(range(-1000,45000))
    transform= lambda x: x*slope +intercept
    yVals= transform(xVals)
    plt.plot(xVals,yVals)
    plt.text(
      0,60,
      f'Slope: {round(slope,4)}\nY-Intercept: {round(intercept,4)}'
    )
    plt.title(f"{b}\n r ={round(boroData['Cases'].corr(boroData['Attendance%']),4)}")
    
    plt.savefig(
      f"graphs/covidAttendance{b}{extraText}.png",
      bbox_inches="tight",
      dpi=300,
      transparent=True
    )
    # plt.show()
    plt.close()

covidScatter(covidAttendance)

covidDf= covidAttendance.loc[covidAttendance['Cases']!=0]
# print(covidDf)
covidScatter(covidDf, "")