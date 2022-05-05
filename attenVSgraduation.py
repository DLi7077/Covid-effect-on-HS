import time
import pandas as pd
from boroughs import *
start = time.time()


def charToBoro(dbn:str):
  boroMap = {
    'K': 'Brooklyn',
    'R': 'Staten Island',
    'Q': 'Queens',
    'X': 'Bronx',
    'M': 'Manhattan'
  }
  return boroMap[dbn[2]]

# The annual data is pretty clean
# We can extract the needed info with some basic cleaning
def createDataframe(file_name,year:int):
  df = pd.read_csv(file_name)
  
  df= df.dropna(subset=['graduation_rate','attendance_rate','total_students'])
  df['Borough']= df['dbn'].apply(charToBoro)
  
  cols= ['school_name','attendance_rate','graduation_rate','Borough','total_students']
  df = df[cols]
  df['year'] = str(year) # convert to string be to categorical instead of discrete data
  return df.sort_values(by='Borough').reset_index(drop=True)
import json
# let's build a dictionary that maps each year to its respective dataframe
hsData:dict= {
}
for i in range(2017,2022):
  # for each year in 2017-2021, create dataframe for the year
  hsData[i] = createDataframe(f'data/{i}_DOE_High_School_Directory.csv',i)
  hsData[i].to_json(r'jsonData/'+f'{i}'+r'.json',orient="table")
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# # histogram for graduation
# def plotHistogram(data:pd.DataFrame,year, colName, ylim):
#   plt.figure()
#   # some stats for text
#   gradRates= data[colName]
#   mean= round(gradRates.mean(),4)
#   median= gradRates.median()
#   std= round(gradRates.std(),4)
#   studentCount = data['total_students'].sum()
#   avgStudentCount = round(studentCount/len(data),1)
  
#   binRange = np.arange(0,1.05,.025)
#   xLabels= np.arange(0,1.1,.1)
  
#   # plot the histogram
#   histogram= sns.histplot(
#     data= data,
#     x= colName,
#     bins= binRange,
#     hue= 'Borough',
#     multiple='stack'
#   )
#   histogram.set_xticks(xLabels)
#   histogram.set_xlabel(colName, fontsize = 20)
#   histogram.set_ylabel("Schools", fontsize = 20)
  
#   histogram.set(
#     xlim=(.3,1.1),
#     ylim=(0,ylim)
#   )
#   histogram.set_title(
#     f'{year} {colName}'
#   )
#   histogram.text(
#     0.31,# x location
#     30, # y location
#     f'\nMean:{mean}\nMedian:{median}\nStandard Dev:{std}\nStudent Count: {studentCount}\nAVG student Count: {avgStudentCount}',
#     size='large'
#   )
#   sns.move_legend(histogram, "upper right",bbox_to_anchor=(1.1, 1))
#   # plt.savefig(
#   #   f"graphs/{colName}{year}.png",
#   #   bbox_inches="tight",
#   #   dpi=300,
#   #   transparent=True
#   # )
#   plt.close()


# def plotAttendance(data:pd.DataFrame,year):
#   plt.figure()
#   attenRates= data['attendance_rate']
#   mean= round(attenRates.mean(),4)
#   median= attenRates.median()
#   std= round(attenRates.std(),4)
#   studentCount = data['total_students'].sum()
#   avgStudentCount = round(studentCount/len(data),1)
  
#   binRange=np.arange(0.5,1.05, 0.025)
#   xLabels= np.arange(0.5,1.05,0.1)
  
#   ar= sns.histplot(
#     data=data,
#     x='attendance_rate',
#     bins= binRange,
#     hue= 'Borough',
#     multiple='stack'
#   )
  
#   ar.set_xticks(xLabels)
#   ar.set_xlabel("Attendance Rate", fontsize = 20)
#   ar.set_ylabel("Schools", fontsize = 20)
#   ar.set(
#     xlim=(.5,1.1),
#     ylim=(0,100)
#   )
  
#   ar.set_title(
#     f'{year} Attendance Distribution'
#   )
#   ar.text(
#     0.51,# x location
#     30, # y location
#     f'\nMean:{mean}\nMedian:{median}\nStandard Dev:{std}\nStudent Count: {studentCount}\nAVG student Count: {avgStudentCount}',
#     size='large'
#   )
  
#   sns.move_legend(ar, "upper right",bbox_to_anchor=(1.1, 1))
  
#   # plt.savefig(
#   #   f"graphs/Attendance_Rates{year}.png",
#   #   bbox_inches="tight",
#   #   dpi=300,
#   #   transparent=True
#   # )
#   plt.close()

# # use changes to record changes in linear regression
# changes =[0,0]
# def plotScatter(
#   df: pd.DataFrame, xCol:str='attendance_rate', yCol:str='graduation_rate',
#   hueCol:str = 'Borough', year:int= 2020):
  
#   plt.figure()
#   correlation= df[xCol].corr(df[yCol])
#   scatterPlot= sns.scatterplot(
#     data= df,
#     x=xCol,
#     y=yCol,
#     hue=hueCol,
#     alpha=0.69
#   )
  
#   scatterPlot.set(
#     title= (
#       f'Attendance vs Graduation Rates {year}\nr={round(correlation,4)}, r^2= {round(correlation**2,4)}'),
#     xlim= (0.6,1.05),
#     ylim= (0.2,1.05)
#   )
#   scatterPlot.set_xlabel("Attendance Rate", fontsize = 20)
#   scatterPlot.set_ylabel("Graduation Rate", fontsize = 20)
  
#   sns.move_legend(scatterPlot, "lower right")
  
#   # get regression line 
#   from statModels import computeLinearReg
#   slope, intercept= computeLinearReg(df,xCol,yCol)
  
#   #plot regression line
#   xVals= np.array(range(100))
#   transform= lambda x: x*slope +intercept
#   yVals= transform(xVals)
#   plt.plot(xVals,yVals)
#   changes[0] = intercept- changes[0]
#   changes[1] = slope- changes[1]
#   if(changes[0]==intercept):
#     changes[0]=0
#     changes[1]=0
#   plt.text(
#     .61,0.75,
#     f'Slope: {round(slope,4)}'
#     +f'\n Change: {round(changes[1],4)}\n'
#     +f'\n Y-Intercept: {round(intercept,4)}'
#     +f'\n Change: {round(changes[0],4)}'
#   )
#   changes[0]= intercept
#   changes[1]= slope
  
#   # plt.savefig(
#   #   f"graphs/AttenvGrad{year}.png",
#   #   bbox_inches="tight",
#   #   dpi=300,
#   #   transparent=True
#   # )
#   # plt.show()
#   plt.close()

# # saves image of student distribution across boroughs
# def studentPieChart(df: pd.DataFrame,year):
#   plt.figure()
#   grouped= df.groupby('Borough').sum()['total_students'].astype(int).reset_index()
#   boroughs= grouped['Borough'].tolist()
#   students= grouped['total_students'].tolist()
  
#   colors= sns.color_palette('pastel')
#   plt.pie(students,labels= boroughs,colors= colors, autopct='%0.0f%%')
#   plt.title(f'Student Distribution {year}')
#   # plt.savefig(
#   #   f"graphs/studentDistribution{year}.png",
#   #   bbox_inches="tight",
#   #   dpi=300,
#   #   transparent=True)
#   plt.close()
  

# # show Graduation vs Attendance per year
# year= 2017
# for data in hsData.values():
#   plotHistogram(data,year,'graduation_rate',50)
#   plotHistogram(data,year,'attendance_rate',100)
  
#   # does attendance correlate with graduation rate?
#   plotScatter(data,'attendance_rate','graduation_rate',year=year)
  
#   studentPieChart(data,year)
#   year+=1

# overall Graduation and Attendance for each year
# totalData= pd.DataFrame()
# for year in range(2017,2022):
#   yearDF= hsData[year]
  
#   # get yearly summary for each borough
#   annualBoros= pd.DataFrame()
#   for b in boroList:
#     yearBoro= yearDF.loc[yearDF['Borough']==b]
#     attAvg = yearBoro['attendance_rate'].mean()
#     gradAvg= yearBoro['graduation_rate'].mean()
#     annualBoros= pd.concat([
#       annualBoros,
#       pd.DataFrame({
#         'Borough':b,
#         'attendance_rate': attAvg,
#         'graduation_rate':gradAvg,
#         'year': year
#       },index=[0]) 
#     ])
#   annualBoros = annualBoros.reset_index(drop=True)
#   totalData= pd.concat([totalData,annualBoros])
# totalData= totalData.reset_index(drop=True)

# print(totalData)
end = time.time()
print(f"Runtime : {end - start}")