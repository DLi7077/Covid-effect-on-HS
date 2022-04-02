import pandas as pd
import re
import boroughs
"""
given a highschool csv file with the columns: 
school name, borocode, language_classes, advanced placement courses,
location, subway, bus, total_students, start_time, end_time, psal_sports_boys,
psal_sports_girls, psal_sports_coed,
graduation_rate, attendance_rate, college_career_rate

create dataframe to only those columns,
drop schools without reported graduation rates
"""

# createDataFrame (constructor)
def createDataFrame(year:int) -> pd.DataFrame:
    df= pd.read_csv(f'data/{year}_DOE_High_School_Directory.csv')
    df= df.rename(columns={"boro": "borocode"})
    
    filter_cols= ["school_name","borocode", "language_classes",
    "advancedplacement_courses","location","subway","bus",
    "total_students","start_time","end_time","psal_sports_boys","psal_sports_girls","psal_sports_coed",
    "graduation_rate","attendance_rate","college_career_rate"]
    df=df[filter_cols]
    df=df.dropna(subset=['graduation_rate'], inplace = False)
    return df

# Borough filters: return df of highschools of requested borough (boro)
def schoolBoro(df, boro) -> pd.DataFrame:
    boro = boro.lower() #lowercase so its not case sensitive
    boroList=['bronx','brooklyn','staten island','manhattan','queens']
    if(not boro in boroList):
        print(boro, 'is an invalid borough')
        print('expected:\n', boroList)
        quit()
    boroMap= {
        'bronx':'X',
        'brooklyn': 'K',
        'staten island': 'R',
        'manhattan': 'M',
        'queens': 'Q'
    }
    return df.loc[df['borocode']==boroMap[boro]].reset_index()


# creates df that contains the graduation rate for each year
def graduationDf():
    df= pd.DataFrame()
    # append yearly data, given a yearly dataframe
    def annualGR(yearlyDF,year):
        newRow:dict= {'year':year}
        for b in boroughs.boros:
            avgGR= avgGraduationRate(schoolBoro(yearlyDF,b))
            newRow[b]=round(avgGR,2)
        # print(newRow)
        return pd.DataFrame(newRow, index=[year-2017])
    
    # add every year to new DF
    for i in range(2017, 2022):
        yearDF= annualGR(createDataFrame(i),i)
        df= pd.concat([df,yearDF])
    return df
    

# Given a school term dataframe, return the average Graduation Rate
def avgGraduationRate(df) -> float:
    return df['graduation_rate'].mean()


#----------- BUS FUNCTIONS -----------
# get dictionary of buses and the amount of schools they're near
def getBusFreq(df: pd.DataFrame) -> dict:
    busFreq:dict = {}
    for i, busList in df['bus'].items():
        rawText= busList.replace(',','')
        buses= rawText.split(' ')
        for bus in buses:
            if(bus in busFreq):
                busFreq[bus]+=1
            else:
                busFreq[bus]=1
    return busFreq

# avg amount of bus routes per school in given df
def avgBusRoutes(df) -> int:
    busRouteSeries= df['bus']
    busRoutes=0
    for busList in busRouteSeries.iteritems():
        busRoutes+= len(str(busList).split(','))
    avgBusRoutes= busRoutes/len(busRouteSeries)
    return avgBusRoutes

# top (default) 3 most common bus routes for schools in given df
def popularBusRoutes(df, limit =5) -> list:
    busMap= getBusFreq(df)
    busMap =sorted(busMap.items(), key= lambda x: x[1], reverse= True)
    busMap= list(dict(busMap).keys())
    popular =[]
    for i in range(limit):
        popular.append(busMap[i])
    return popular


#-----------TRAIN FUNCTIONS-----------

# use regex expressions to extract train routes
def extractTrains(trainText: str)-> list:
    regex= r'[A-Z0-9] {1}'
    trainText=trainText.replace(',', ' ')
    trainText=trainText.replace(';',' ')
    results= re.findall(regex,trainText)
    return results

# maps out subway frequency to a map
def getSubwayFreq(df: pd.DataFrame) -> dict:
    trainFreq= {}
    subwaySeries= df['subway'].dropna()
    for i, trainList in subwaySeries.items():
        print(trainList)
        trains= extractTrains(trainList)
        for t in trains:
            if (t in trainFreq):
                trainFreq[t]+=1
            else:
                trainFreq[t]=1
    return trainFreq

# avg amount of subway routes per school in given df
def avgSubwayRoutes(df:  pd.DataFrame) -> int:
    subwayRoutes=0
    for i, subwayList in df['subway'].items():
        trains= extractTrains(subwayList)
        subwayRoutes+=len(trains)

    avgSubwayRoutes= subwayRoutes/len(df['subway'])
    return avgSubwayRoutes

# top (default) 3 most common subway routes for schools in given df
def popularSubwayRoutes(df,limit= 3) -> list:
    subwayRouteSeries= df['subway']
    subwayRoutes = {}

    return

# print(help(pd.Series.iteritems))
# print(help(dict))
