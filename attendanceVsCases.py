"""_summary_
compares cases with boro attendance on a scatter plot. saves graphs as png image
"""

import pandas as pd
from attendance import AttendanceDf, data2021
from covidData import cases
from statModels import computeLinearReg
import numpy as np

# merge the covid and cases dataframe
AttendanceDf= AttendanceDf.drop(columns=['Month'])
AvC= pd.merge(AttendanceDf,cases, how= 'outer', on ='Date')
AvC= AvC.fillna(0)
# collective covid and avg attendance cases per month

from boroughs import bList
import seaborn as sns
import matplotlib.pyplot as plt
# modify the cols 

df= pd.DataFrame()
for b in bList:
  att = (AvC[f'{b} Attendance%']).tolist()
  dates= (AvC['Date']).tolist()
  covidCases= (AvC[b]).tolist()
  
  
  for i in range(len(att)):
    row=pd.DataFrame({
      'Borough': b,
      'Attendance%': att[i],
      'Date':dates[i],
      'cases':covidCases[i]
    },index= [0])
    df = pd.concat([df,row])
df= df.reset_index(drop= True)
  

plt.figure()

# Attendance Timeline
df= df.dropna()
df= df.loc[ df['Attendance%']!=0]
print(df)
Att= sns.scatterplot(
  data= df,
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
plt.show()

# covid vs attendance rate scatterplot
def covidScatter(covidDf,extraText:str= "withPrev"):
  plt.figure()
  cases= sns.scatterplot(
    data= covidDf,
    x='cases',
    y='Attendance%',
    hue= 'Borough'
    # ,
    # x_jitter=200,
    # scatter_kws={'alpha':0.5},
    # fit_reg=False
  )
  cases.set(
    xlim=(-1000,45000),
    ylim=(50, 100),
  )
  plt.legend(loc='lower left')
  slope, intercept = computeLinearReg(covidDf,'cases','Attendance%')

  xVals= np.array(range(-1000,45000))
  transform= lambda x: x*slope +intercept
  yVals= transform(xVals)
  plt.plot(xVals,yVals)
  plt.text(
    30000,60,
    f'Slope: {round(slope,4)}\nY-Intercept: {round(intercept,4)}'
  )
  plt.title( f"All Boroughs\nr= {round(covidDf['cases'].corr(covidDf['Attendance%']),4)}")
  plt.savefig(
    f"graphs/covidAttendanceAll{extraText}.png",
    bbox_inches="tight",
    dpi=300,
    transparent=True
  )
  plt.close()
  from boroughs import boroColor
  for b in bList:
    plt.figure()
    boroData= covidDf.loc[covidDf['Borough']==b]
    cases= sns.regplot(
      data= boroData,
      x='cases',
      y='Attendance%',
      color=boroColor[b],
      x_jitter=500,
      scatter_kws={'alpha':0.5}
    )
    # plt.scatter(boroData['cases'], boroData['Attendance%'], c=boroColor[b])
    cases.set(
    xlim= (-1000, 45000),
    ylim=(50, 100),
    )
    slope, intercept = computeLinearReg(boroData,'cases','Attendance%')
    
    xVals= np.array(range(-1000,45000))
    transform= lambda x: x*slope +intercept
    yVals= transform(xVals)
    plt.plot(xVals,yVals)
    plt.text(
      0,60,
      f'Slope: {round(slope,4)}\nY-Intercept: {round(intercept,4)}'
    )
    plt.title(f"{b}\n r ={round(boroData['cases'].corr(boroData['Attendance%']),4)}")
    
    plt.savefig(
      f"graphs/covidAttendance{b}{extraText}.png",
      bbox_inches="tight",
      dpi=300,
      transparent=True
    )
    # plt.show()
    plt.close()

covidScatter(df)

covidDf= df.loc[df['cases']!=0]
covidScatter(covidDf, "")