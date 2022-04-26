# cleaning up time columns:
# df should contain a Year and Month column
# merge them to datetime with the day being the last day of the month
import pandas as pd
from pandas.tseries.offsets import MonthEnd # for end of month date
def cleanDate(df):
    copy= df
    ser= pd.to_datetime(
        copy[['Year','Month']].assign(DAY=1)
    )
    copy['Date']= pd.to_datetime(
        ser,format='%Y-%m'
        ) +MonthEnd(1)
    
    return copy.drop(columns = ['Year','Month'])
    # return df
