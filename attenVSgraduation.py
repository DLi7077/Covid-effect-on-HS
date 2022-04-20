import time
import pandas as pd
from sklearn import linear_model

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

# cleans csv to borough, year, attendance, and grad rate
def createDataframe(file_name,year:int):
  df = pd.read_csv(file_name)
  df= df.dropna(subset=['graduation_rate','attendance_rate','total_students'])
  df['Borough']= df['dbn'].apply(charToBoro)
  cols= ['attendance_rate','graduation_rate','Borough','total_students']
  df = df[cols]
  df['year'] = str(year)
  return df.sort_values(by='Borough')

hsData:dict= {
}
for i in range(2017,2022):
  hsData[i] = createDataframe(f'data/{i}_DOE_High_School_Directory.csv',i)

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def plotGraduation(data:pd.DataFrame,year):
  plt.figure()
  gradRates= data['graduation_rate']
  mean= round(gradRates.mean(),4)
  median= gradRates.median()
  std= round(gradRates.std(),4)
  studentCount = data['total_students'].sum()
  avgStudentCount = round(studentCount/len(data),1)
  
  binRange = np.arange(0,1.05,.025)
  xLabels= np.arange(0,1.1,.1)
  
  gr= sns.histplot(
    data= data,
    x= 'graduation_rate',
    bins= binRange,
    hue= 'Borough',
    multiple='stack'
  )
  gr.set_xticks(xLabels)
  gr.set_xlabel("Graduation Rate", fontsize = 20)
  gr.set_ylabel("Schools", fontsize = 20)
  
  gr.set(
    xlim=(.3,1.1),
    ylim=(0,50)
  )
  gr.set_title(
    f'{year} Graduation Distribution'
  )
  gr.text(
    0.31,# x location
    30, # y location
    f'\nMean:{mean}\nMedian:{median}\nSample Dev:{std}\nStudent Count: {studentCount}\nAVG student Count: {avgStudentCount}',
    size='large'
  )
  sns.move_legend(gr, "upper right",bbox_to_anchor=(1.1, 1))
  plt.savefig(
    f"graphs/Graduation_Rates{year}.png",
    bbox_inches="tight",
    dpi=300,
    transparent=True
    )
  plt.close()
  
def plotAttendance(data:pd.DataFrame,year):
  plt.figure()
  attenRates= data['attendance_rate']
  mean= round(attenRates.mean(),4)
  median= attenRates.median()
  std= round(attenRates.std(),4)
  studentCount = data['total_students'].sum()
  avgStudentCount = round(studentCount/len(data),1)
  
  binRange=np.arange(0.5,1.05, 0.025)
  xLabels= np.arange(0.5,1.05,0.1)
  
  ar= sns.histplot(
    data=data,
    x='attendance_rate',
    bins= binRange,
    hue= 'Borough',
    multiple='stack'
  )
  
  ar.set_xticks(xLabels)
  ar.set_xlabel("Attendance Rate", fontsize = 20)
  ar.set_ylabel("Schools", fontsize = 20)
  ar.set(
    xlim=(.5,1.1),
    ylim=(0,100)
  )
  
  ar.set_title(
    f'{year} Attendance Distribution'
  )
  ar.text(
    0.51,# x location
    30, # y location
    f'\nMean:{mean}\nMedian:{median}\nSample Dev:{std}\nStudent Count: {studentCount}\nAVG student Count: {avgStudentCount}',
    size='large'
  )
  
  sns.move_legend(ar, "upper right",bbox_to_anchor=(1.1, 1))
  
  plt.savefig(
    f"graphs/Attendance_Rates{year}.png",
    bbox_inches="tight",
    dpi=300,
    transparent=True
  )
  plt.close()

def plotScatter(
  df: pd.DataFrame, xCol:str='attendance_rate', yCol:str='graduation_rate',
  hueCol:str = 'Borough', year:int= 2020):
  
  plt.figure()
  correlation= df[xCol].corr(df[yCol])
  scatterPlot= sns.scatterplot(
    data= df,
    x=xCol,
    y=yCol,
    hue=hueCol
  )
  
  scatterPlot.set(
    title= (
      f'Attendance vs Graduation Rates {year}\nr={round(correlation,4)}, r^2= {round(correlation**2,4)}'),
    xlim= (0.6,1.05),
    ylim= (0.2,1.05)
  )
  scatterPlot.set_xlabel("Attendance Rate", fontsize = 20)
  scatterPlot.set_ylabel("Graduation Rate", fontsize = 20)
  
  sns.move_legend(scatterPlot, "lower right")
  
  plt.savefig(
    f"graphs/AttenvGrad{year}.png",
    bbox_inches="tight",
    dpi=300,
    transparent=True
  )
  plt.close()

def plotJoint(
  df: pd.DataFrame, xCol:str='attendance_rate', yCol:str='graduation_rate'
):
  joint= sns.JointGrid(
    data= df,
    x=xCol,
    y=yCol,
    kind= 'kde'
  )
  correlation= df[xCol].corr(df[yCol])
  joint.set(title= f'r= {round(correlation,4)}')
  
  plt.close()
  return joint

# saves image of student distribution across boroughs
def studentPieChart(df: pd.DataFrame,year):
  plt.figure()
  grouped= df.groupby('Borough').sum()['total_students'].astype(int).reset_index()
  boroughs= grouped['Borough'].tolist()
  students= grouped['total_students'].tolist()
  
  colors= sns.color_palette('pastel')
  plt.pie(students,labels= boroughs,colors= colors, autopct='%0.0f%%')
  plt.title(f'Student Distribution {year}')
  plt.savefig(
    f"graphs/studentDistribution{year}.png",
    bbox_inches="tight",
    dpi=300,
    transparent=True)
  plt.close()
  

# show Graduation vs Attendance per year
year= 2017
for data in hsData.values():
  plotGraduation(data,year)
  
  plotAttendance(data,year)
  
  # does attendance correlate with graduation rate?
  plotScatter(data,'attendance_rate','graduation_rate',year=year)
  
  studentPieChart(data,year)
  year+=1




# overall Graduation and Attendance
totalData= pd.DataFrame()
for data in hsData.values():
  totalData= pd.concat([totalData,data])

totalData= totalData.reset_index().drop(columns=['index'])

print(totalData)
print(studentPieChart(totalData,2020))

# randomArray= np.random.randint(2004,size=250)
# print(randomArray)
# # print(totalData)
# # total time taken
# plotScatter(totalData.iloc[randomArray],hueCol='year')

# plt.show()

# def LinearRegModel(x_train,y_train):
#   linearReg= linear_model.LinearRegression()
#   linearReg.fit(x_train,y_train)
#   return linearReg

# from sklearn.preprocessing import PolynomialFeatures
# def transform_numeric_cols(df_num, degree_num=2) -> np.ndarray:
#   polyPredict= PolynomialFeatures(degree=degree_num, include_bias=False)
#   npValues= polyPredict.fit_transform(df_num)
#   return npValues

# from sklearn.model_selection import train_test_split


# x_train,x_test,y_train,y_test = train_test_split(totalData,totalData)


end = time.time()
print(f"Runtime : {end - start}")