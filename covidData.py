import pandas as pd
import re
import boroughs

# create dataframe
#borough filters
def createDataFrame():
    file_name= 'data\COVID-19_Daily_Counts_of_Cases__Hospitalizations__and_Deaths.csv'
    df = pd.read_csv(file_name)
    return df
# Borough filters: return df
def boroCovidData(df: pd.DataFrame, boro: str)-> pd.DataFrame:
    boro = boro.lower() #lowercase so its not case sensitive
    boroList=['bronx','brooklyn','staten island','manhattan','queens']
    
    if(not boro in boroList):
        print(boro, 'is an invalid borough')
        print('expected:\n', boroList)
        quit()
    
    boroMap= {
        'bronx':'BX',
        'brooklyn': 'BK',
        'staten island': 'SI',
        'manhattan': 'MN',
        'queens': 'QN'
    }
    
    boroKey= r''+boroMap[boro]+'.+'
    isAvgCol= r'^.+AVG'
    boroColumns= ['DATE_OF_INTEREST']
    for colName in df.columns:
        if(re.match(boroKey,colName) is not None
           and not re.match(isAvgCol,colName)):
            boroColumns.append(colName)
    return df[boroColumns]

# get the totalCaseCount of a given covid df
def totalCaseCount(df: pd.DataFrame)-> int:
    caseCountCols=[]
    regex= r'.+CASE_COUNT' # to match columns that contain cases
    for colName in df.columns:
        if(colName=='CASE_COUNT'): #Case_count will exist if boroughs not filtered
            caseCountCols= ['CASE_COUNT']
            break
        elif(re.match(regex,colName) is not None):
            caseCountCols.append(colName)
    totalCases= 0
    for col in caseCountCols:
        totalCases+= df[col].sum()
    return totalCases

            

# params: 
#   df: a dataframe with a 'DATE_OF_INTEREST' and '.._CASE_COUNT' columns
#   year: integer representing year
# returns:
#   the amount of cases at the end of the given school year
# instead of ending at 12-21-XXXX, it will end at June-27-XXXX
# 2022 Term Calendar: https://www.schools.nyc.gov/about-us/news/2021-2022-school-year-calendar
def covidbySchoolYear(df: pd.DataFrame, year: int)-> int:
    year= int(year)
    if(int(year)<2019): # no cases prior to 2020
        print('NOTE: Covid-19 Cases appeared in 2020')
        return pd.DataFrame()
    
    # set bounds that define the school year (including summer)
    lowerBound_date= (str(year-1)+'-6-27')
    upperBound_date= (str(year) + '-6-27')
    
    # extract case count
    df['DATE_OF_INTEREST']= pd.to_datetime(df['DATE_OF_INTEREST'])
    schoolTerm = df[(df['DATE_OF_INTEREST']>= lowerBound_date) 
                & (df['DATE_OF_INTEREST']< upperBound_date)]
    
    return schoolTerm




# Create a dataframe that summarizes covid cases by school year
def covidSummaryDF():
	df = pd.DataFrame()
	data= createDataFrame()

# takes a yearly df of covid cases and returns a simplified row
	def annualCovid(yearlyDF, year):
		if(year<2020):
			newRow= {
				'school_year':year,
				'bronx': 0,
				'brooklyn': 0,
				'staten island': 0,
				'manhattan': 0,
				'queens':0
			}
			return pd.DataFrame(newRow, index= [year-2017])
		newRow:dict= {'school_year': year}
		# add each borough to newRow
		for b in boroughs.boros:
			yearlyData= boroCovidData(yearlyDF,b)
			# add new col to row
			newRow[b]=totalCaseCount(yearlyData)
   
   		# this is one year's covid data
		return pd.DataFrame(newRow, index=[year-2017])
	
	# add each year [2017,2022]'s data to the resulting df
	for year in range(2017,2023):
		yearAsRow= annualCovid(covidbySchoolYear(data,year), year)
		df= pd.concat([df,yearAsRow])

	return df

    