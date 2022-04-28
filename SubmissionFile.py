"""
Resources:
accessing groupby object
https://stackoverflow.com/questions/14734533/how-to-access-pandas-groupby-dataframe-by-key
groupby month and year
https://stackoverflow.com/questions/26646191/pandas-groupby-month-and-year
to_numeric
https://pandas.pydata.org/docs/reference/api/pandas.to_numeric.html
"""

import pandas as pd
from boroughs import *
import re
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

"""_summary_
creates a monthly attendance dataframe by combining multiple csv files and cleaning up data
returns df with cols:
[
    Bronx Attendance%,
    Brooklyn Attendance%,
    Manhattan Attendance%,
    Queens Attendance%,
    Staten Island Attendance%,
    Month(# of months since sept. 2018),
    Date(# end of month date)
]
"""
# helper function to translate months to date
from pandas.tseries.offsets import MonthEnd # for end of month date
def cleanDate(df):
		dateSeries= pd.to_datetime(
				df[['Year','Month']].assign(DAY=1)
		)
		df['Date']= pd.to_datetime(
				dateSeries,format='%Y%m'
				) +MonthEnd(1)
		
		return df.drop(columns = ['Year','Month'])

def attendanceDataframe():
	def keyToBoro(boro:str)->str:
			boroMap= {
			'X':'Bronx',
			'K':'Brooklyn',
			'R':'Staten Island',
			'M':'Manhattan',
			'Q':'Queens'
			}
			return boroMap[boro[2]]

	# mass attendance data from 2018-part of 2020
	def createAttendanceDataframe()-> pd.DataFrame:
			df =pd.read_csv('attendance/2018-2021_Daily_Attendance_by_School.csv')
			df['Date'] =pd.to_datetime(df['Date'])
			# identifies school borough based on school DBN
			# DBN will be 6 digits, where the 3rd character is the boroCode

			df['Borough']= df['School DBN'].apply(keyToBoro)
			df= df.drop(columns=['School DBN','SchoolYear'])
			df['Year']= df['Date'].dt.year
			df['Month'] =df['Date'].dt.month
			df= df.groupby(['Year','Month','Borough']).sum()
			df['Attendance%'] = 100*(df['Present']/(df['Present']+df['Absent']+df['Released']))
			df= df.drop(columns= ['Enrolled','Present','Absent','Released'])
			return df.reset_index()

	# attendance from 2021 (remote learning), but the data is clean
	# returns a df Row, containing each boro's average attendance for that month
	def data2021(df):
			df= df.rename(columns={'Overall Attendance Rate':'Attendance%'})
			df['Borough'] =df['DBN'].apply(keyToBoro)
			df= df[['Borough','Attendance%']]
			df= df.groupby('Borough').mean()
			return df.reset_index()

	# attendance from 2021 (remote learning), but the data has unneeded categories
	# returns a df Row, containing each boro's average attendance for that month
	def ugly2021(df):
			df= df[['Geographic Unit','Student Category 1','Overall Attendance Rate']]
			df= df.rename(columns={'Overall Attendance Rate':'Attendance%'})
			# some values are labeled s
			df= df.loc[df['Attendance%']!='s']
			df['Attendance%']=df['Attendance%'].astype('float64')

			# target highschool students
			highschoolStudents= ['Grade 09','Grade 10','Grade 11','Grade 12']
			df= df.loc[df['Student Category 1'].isin(highschoolStudents)]
			# target schools in valid districts
			
			
			# if the value has district in name, then it's a district
			def isDistrict(unit:str):
					return 'District' in unit
			df= df.loc[df['Geographic Unit'].apply(isDistrict)]
			df= df[['Geographic Unit', 'Attendance%']]

			# helper function to convert district to borough
			# https://data.nysed.gov/profile.php?instid=7889678368
			def districtBorough(num: int):
					id = int(num[9:])
					districtMap= {
							1 : 'Manhattan',
							2 : 'Manhattan',
							3 : 'Manhattan',
							4 : 'Manhattan',
							5 : 'Manhattan',
							6 : 'Manhattan',
							7 : 'Bronx',
							8 : 'Bronx',
							9 : 'Bronx',
							10 : 'Bronx',
							11 : 'Bronx',
							12 : 'Bronx',
							13 : 'Brooklyn',
							14 : 'Brooklyn',
							15 : 'Brooklyn',
							16 : 'Brooklyn',
							17 : 'Brooklyn',
							18 : 'Brooklyn',
							19 : 'Brooklyn',
							20 : 'Brooklyn',
							21 : 'Brooklyn',
							22 : 'Brooklyn',
							23 : 'Brooklyn',
							24 : 'Queens',
							25 : 'Queens',
							26 : 'Queens',
							27 : 'Queens',
							28 : 'Queens',
							29 : 'Queens',
							30 : 'Queens',
							31 : 'Staten Island',
							32 : 'Brooklyn',
							75 : 'idk',
							79 : 'idk'
					}
					return districtMap[id]
			# translate district to boroughs
			df['Borough'] = df['Geographic Unit'].apply(districtBorough)
			# choose boroughs with valid matching
			df= df.loc[df['Borough']!='idk']
			df.rename(columns={'Geographic Unit':'Borough'})

			# merge borough attendance rates
			df= df.groupby('Borough').mean()
			df= df.reset_index()

			return df

	# create dataframes and merge them
	# Base Empty Dataframe:
	baseDF= createAttendanceDataframe()

	# extra months files that we can add for 2021:
	monthList = {'01','02','03','04','05','09','10'}

	# append the extra months
	for month in monthList:
			file_name= f'attendance/{month}_2021.csv'
			df = pd.read_csv(file_name)
			if('DBN' in df.columns): # file isnt ugly, read normally
					df = data2021(df)
			else:
					df= ugly2021(df)

			# figure out the date from the month
			regex= r'/.+\.'
			date= (re.findall(regex,file_name)[0][1:-1]).split('_')
			df['Year']= int(date[1])
			df['Month']= int(date[0])

			# add the extra data
			baseDF= pd.concat([baseDF,df])

	# rearrange the dataframe
	# new cols will be [boro0,boro1,boro2,... date, months]
	# let 'Months' col represent the amount of months since Sept 2018
	baseDF['Months']= (baseDF['Month']-9 + 12*(baseDF['Year'] -2018))

	# now to make Month and Year plottable:

	baseDF= cleanDate(baseDF)
	baseDF= baseDF.sort_values(by=['Months','Borough'])

	AttendanceDF= pd.DataFrame()

	# for all rows in baseDF, spread it out to 1 row
	for idx in range(0,len(baseDF),5):
			rowEntry= baseDF.iloc[idx:idx+5].reset_index()
			cols = rowEntry['Borough'].tolist()
			attendance= rowEntry['Attendance%'].tolist()

			newRow= {}
			
			for i in range(len(cols)):
					newRow[f'{cols[i]} Attendance%']= attendance[i]

			newRow['Month']= baseDF.iloc[idx,2]
			newRow['Date'] =baseDF.iloc[idx,3]
			newRow= pd.DataFrame(newRow,index=[idx])

			AttendanceDF=pd.concat([AttendanceDF,newRow])

	AttendanceDF=AttendanceDF.reset_index(drop=True)

	# problem: some dates are left out bc of summer/ breaks
	# manually add the months and set the attendance to be 0

	monthSet= set(np.arange(38))

	# removing existing months
	for i,row in AttendanceDF['Month'].iteritems():
		if(row in monthSet):
			monthSet.remove(row)

	# add each missing month
	for m in monthSet:
		newRow = {}
		for b in boroSet:
			newRow[f'{b} Attendance%']=0
		newRow['Month']=m
		
		# we start at september, so consider +9 to calculation
		actualMonth= (m+9)%12
		if(actualMonth==0):
			actualMonth= 12
		actualYear= 2018+(m+9)//12
		newRow['Date']= pd.to_datetime(f'{actualYear}-{actualMonth}', format= '%Y-%m')+MonthEnd(1)
		newRow= pd.DataFrame(newRow, index= [0])
		AttendanceDF= pd.concat([AttendanceDF,newRow])

	return AttendanceDF.sort_values(by= ['Month','Date']).reset_index(drop=True)
	
# finally done. Data is cleaned and now  we have each borough's avg attendance rate per month
# Unfortunately, this is only from 2018- to Oct 2021, with a missing chunk in 2020 due to attendance not being taken during covid

# store AttendanceDF
AttendanceDF= attendanceDataframe()

# ------------------COVID DATA----------------------------------------------------------------------------------------------------
"""_summary_
	Functions to aid with data fetching from covid dataframe

createCovidDataframe: create dataframe with covid data for the 5 boroughs
getTimeMeasure: returns a list of time Measurements: Date, Month, or Year
queryData: takes one of [Case','Hospitalized','Death'], returns the dataframe of provided queryKey
queryBoro: filters dataframe for borough
monthlyData: aggregates data into months
"""
# create dataframe with covid Data
def createCovidDataframe():
    file_name= 'data\COVID-19_Daily_Counts_of_Cases__Hospitalizations__and_Deaths.csv'
    df = pd.read_csv(file_name)
    boroList=['Bronx','Brooklyn','Staten Island','Manhattan','Queens']
    boroMap= {
        'Bronx':'BX',
        'Brooklyn': 'BK',
        'Staten Island': 'SI',
        'Manhattan': 'MN',
        'Queens': 'QN'
    }
    boroColumns= ['Date']
    # get the columns with borough information
    for boro in boroList:
        boroKey= r''+boroMap[boro]+'.+'
        isAvgCol= r'^.+AVG'
        for col in df.columns:
            if(re.match(boroKey,col) is not None and not re.match(isAvgCol,col)):
                # get the term associated with the borough: eg case count, death count, hospitalized
                term = re.findall(boroKey,col)[0].split('_')[1:]
                term = f'{term[0].title()} {term[1].title()}'
                neededCol= f'{boro}_{term}'
                
                df= df.rename(columns={
                    col:neededCol
                })
                boroColumns.append(neededCol)
                
            # is time measurement
            elif(col=='Year' or col=='Month' or col=='Date'):
                boroColumns.append(col)
    
    df= df.rename(columns={
        'DATE_OF_INTEREST':'Date'
    })
    df['Date'] = pd.to_datetime(df['Date'],format='%m/%d/%Y')
    return df[boroColumns].reset_index(drop=True)

# before we create helper functions, we should make one that provides the time measurement of the data.
def getTimeMeasure(dfColumns):
    cols=[]
    # has time measurement
    if('Date' in dfColumns):
        cols.append('Date')
        
    elif('Month' in dfColumns):
        cols.append('Month')
        cols.append('Year')
    return cols

# helper function to filterby cases, deaths, and hospitalized
def queryData(df: pd.DataFrame, query:str)->pd.DataFrame:
    queries= [
        'Case',
        'Hospitalized',
        'Death'
    ]
    if (query not in queries):
        raise ValueError(f'query \'{query}\' not in {queries}')
    
    query= query+' Count'
    
    queriedCols=getTimeMeasure(df.columns)
    key= r'.+'+query
    for col in df.columns:
        if (re.match(key,col)is not None):
            # get borough
            borough = col.split('_')[0]
            df= df.rename(columns={
                col:borough
            })
            queriedCols.append(borough)
            
    return df[queriedCols]

# helper function to filterby borough
def queryBoro(df:pd.DataFrame, boro:str):
    boro= boro.title()
    boroCols= getTimeMeasure(df.columns)
        
    for col in df.columns:
        if(boro in col):
            component =col.split('_')[1]
            df= df.rename(columns={
                col:component
            })
            boroCols.append(component)
    return df[boroCols].reset_index(drop=True)

# groups data into months
def monthlyData(df:pd.DataFrame)->pd.DataFrame:
    df['Date'] = pd.to_datetime(df['Date'],format='%m/%d/%Y')
    df['Month']= (df['Date'].dt.month).astype(str)
    df['Year'] = (df['Date'].dt.year).astype(str)
    df= df.groupby(['Year','Month']).sum().reset_index()
    df['Date'] =df['Month']+'-'+df['Year']
    return df

# Plotting timeline of daily cases
covidDataframe = createCovidDataframe()
covidCases= queryData(covidDataframe,'Case')

# reorganize df to have boroughs as rows instead of columns
caseDF = pd.DataFrame()
for b in boroList:
    caseCount= covidCases[b].tolist()
    date= covidCases['Date'].tolist()
    for i in range(len(caseCount)):
        tempRow= pd.DataFrame({
            'Borough': b,
            'Cases' : caseCount[i],
            'Date': date[i]
        },index=[0])
        caseDF= pd.concat([caseDF,tempRow])
    
caseDF=caseDF.reset_index(drop=True)

# Plot daily covid cases
plt.figure()
casePlot = sns.lineplot(
    data= caseDF,
    x='Date', y= 'Cases',
    hue= 'Borough',
    linewidth = .5
)
casePlot.set(yscale='log')
plt.title('New Cases by Day')
plt.xticks(rotation=45)
# plt.savefig(
#     "graphs/CovidCasesDaily.png",
#     bbox_inches="tight",
#     dpi=300,
#     transparent=True
# )
plt.show()
plt.close()

# ------------------------------------------------------------------------------------------------------------------------------
"""_summary_
	Computes Linear Regression of two series in a dataframe
"""
def computeLinearReg(df:pd.DataFrame,xCol,yCol):
  x= df[xCol]
  y= df[yCol]
  
  correlation = x.corr(y)
  
  slope = correlation*(y.std()/x.std())
  yIntercept=y.mean()- x.mean()*slope
  
  return slope, yIntercept

# Compare Attendance Rates with Graduation Rates--------------------------------------------------------------------------------

# The annual data is pretty clean
# We can extract the needed info with some basic translation
def createDataframe(file_name,year:int):
	df = pd.read_csv(file_name)
	
	def charToBoro(dbn:str):
		boroMap = {
			'K': 'Brooklyn',
			'R': 'Staten Island',
			'Q': 'Queens',
			'X': 'Bronx',
			'M': 'Manhattan'
		}
		return boroMap[dbn[2]]

	df= df.dropna(subset=['graduation_rate','attendance_rate','total_students'])
	df['Borough']= df['dbn'].apply(charToBoro)
	
	cols= ['school_name','attendance_rate','graduation_rate','Borough','total_students']
	df = df[cols]
	df['year'] = str(year) # convert to string be to categorical instead of discrete data
	return df.sort_values(by='Borough').reset_index()

# let's build a dictionary that maps each year to its respective dataframe
hsData:dict= {
}
for i in range(2017,2022):
	# for each year in 2017-2021, create dataframe for the year
	hsData[i] = createDataframe(f'data/{i}_DOE_High_School_Directory.csv',i)

# histogram for graduation
def plotHistogram(data:pd.DataFrame,year, colName, ylim):
	plt.figure()
	# some stats for text
	gradRates= data[colName]
	mean= round(gradRates.mean(),4)
	median= gradRates.median()
	std= round(gradRates.std(),4)
	studentCount = data['total_students'].sum()
	avgStudentCount = round(studentCount/len(data),1)
	
	binRange = np.arange(0,1.05,.025)
	xLabels= np.arange(0,1.1,.1)
	
	# plot the histogram
	histogram= sns.histplot(
		data= data,
		x= colName,
		bins= binRange,
		hue= 'Borough',
		multiple='stack'
	)
	histogram.set_xticks(xLabels)
	histogram.set_xlabel(colName, fontsize = 20)
	histogram.set_ylabel("Schools", fontsize = 20)
	
	histogram.set(
		xlim=(.3,1.1),
		ylim=(0,ylim)
	)
	histogram.set_title(
		f'{year} {colName}'
	)
	histogram.text(
		0.31,# x location
		30, # y location
		f'\nMean:{mean}\nMedian:{median}\nStandard Dev:{std}\nStudent Count: {studentCount}\nAVG student Count: {avgStudentCount}',
		size='large'
	)
	sns.move_legend(histogram, "upper right",bbox_to_anchor=(1.1, 1))
	# plt.savefig(
	#   f"graphs/{colName}{year}.png",
	#   bbox_inches="tight",
	#   dpi=300,
	#   transparent=True
	# )
	# plt.show()
	plt.close()

# use changes to record changes in linear regression
changes =[0,0]
def plotScatter(
	df: pd.DataFrame, xCol:str='attendance_rate', yCol:str='graduation_rate',
	hueCol:str = 'Borough', year:int= 2020):
	
	plt.figure()
	correlation= df[xCol].corr(df[yCol])
	scatterPlot= sns.scatterplot(
		data= df,
		x=xCol,
		y=yCol,
		hue=hueCol,
		alpha=0.69
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
	
	# get regression line 
	slope, intercept= computeLinearReg(df,xCol,yCol)
	
	#plot regression line
	xVals= np.array(range(100))
	transform= lambda x: x*slope +intercept
	yVals= transform(xVals)
	plt.plot(xVals,yVals)
	changes[0] = intercept- changes[0]
	changes[1] = slope- changes[1]
	if(changes[0]==intercept):
		changes[0]=0
		changes[1]=0
	plt.text(
		.61,0.75,
		f'Slope: {round(slope,4)}'
		+f'\n Change: {round(changes[1],4)}\n'
		+f'\n Y-Intercept: {round(intercept,4)}'
		+f'\n Change: {round(changes[0],4)}'
	)
	changes[0]= intercept
	changes[1]= slope
	
	# plt.savefig(
	#   f"graphs/AttenvGrad{year}.png",
	#   bbox_inches="tight",
	#   dpi=300,
	#   transparent=True
	# )
	# plt.show()
	plt.close()

# saves image of student distribution across boroughs
def studentPieChart(df: pd.DataFrame,year):
	plt.figure()
	grouped= df.groupby('Borough').sum()['total_students'].astype(int).reset_index()
	boroughs= grouped['Borough'].tolist()
	students= grouped['total_students'].tolist()
	
	colors= sns.color_palette('pastel')
	plt.pie(students,labels= boroughs,colors= colors, autopct='%0.0f%%')
	plt.title(f'Student Distribution {year}')
	# plt.savefig(
	#   f"graphs/studentDistribution{year}.png",
	#   bbox_inches="tight",
	#   dpi=300,
	#   transparent=True)
	plt.close()

# show Graduation vs Attendance per year
year= 2017
for data in hsData.values():
	plotHistogram(data,year,'graduation_rate',50)
	plotHistogram(data,year,'attendance_rate',100)
	
	# does attendance correlate with graduation rate?
	plotScatter(data,'attendance_rate','graduation_rate',year=year)
	
	studentPieChart(data,year)
	year+=1

# overall Graduation and Attendance for every year
totalData= pd.DataFrame()
for data in hsData.values():
	totalData= pd.concat([totalData,data])

totalData= totalData.reset_index(drop=True)

#Compare Attendance Rates vs Cases------------------------------------------------------------------------------------
# merge the covid and cases dataframe
AttendanceDF= AttendanceDF.drop(columns=['Month'])
monthlyCases= cleanDate(monthlyData(covidCases))
# print(monthlyCases)
AvC= pd.merge(AttendanceDF,monthlyCases, how= 'outer', on ='Date')

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
# plt.savefig(
#   f"graphs/AttendanceTimeline.png",
#   bbox_inches="tight",
#   dpi=300,
#   transparent=True
# )
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
  # plt.savefig(
  #   f"graphs/covidAttendanceAll{extraText}.png",
  #   bbox_inches="tight",
  #   dpi=300,
  #   transparent=True
  # )
  plt.show()
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
    
    # plt.savefig(
    #   f"graphs/covidAttendance{b}{extraText}.png",
    #   bbox_inches="tight",
    #   dpi=300,
    #   transparent=True
    # )
    plt.show()
    plt.close()

# scatter attendance based on covid
covidScatter(covidAttendance)

# scatter attendance based on covid (exclude where cases==0)
covidDf= covidAttendance.loc[covidAttendance['Cases']!=0]
covidScatter(covidDf, "")