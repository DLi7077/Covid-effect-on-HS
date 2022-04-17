
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import numpy as np
import pandas as pd

def compute_lin_reg(x,y):
  
  theta_1= x.corr(y)*(y.std()/x.std())  # slope
  theta_0= y.mean() - theta_1*x.mean()  # y-int
  
  return theta_0, theta_1

from sklearn.model_selection import train_test_split
import highschoolData as hs
import covidData as cv
hsData= hs.graduationDf()
covidData= cv.covidSummaryDF()
# predict how well covid affects graduation rates
# for brooklyn:
bkGR= hsData[['year','brooklyn']]
bkCases= covidData[['school_year','brooklyn']]
# drop the cases in 2022 bc theres no grad rates for 2022
bkC= bkCases.loc[bkCases['school_year']<2022]
print(bkC)
print(bkGR)
b, m= compute_lin_reg(bkC['brooklyn'],bkGR['brooklyn'])
print(f'The regression line has slope {m} and y-intercept {b}.')