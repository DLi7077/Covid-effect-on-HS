#borough filters
# for each function, return covid data that's related to the borough.
def boroCovidData(df, boro):
    boro = boro.lower() #lowercase so its not case sensitive
    boroList=['bronx','brooklyn','staten island','manhattan','queens']
    if(not boro in boroList):
        print(boro, 'is an invalid borough')
        print('expected:\n', boroList)
        quit()
        
    return
