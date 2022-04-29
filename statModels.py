import pandas as pd

def computeLinearReg(df:pd.DataFrame,xCol,yCol):
  x= df[xCol]
  y= df[yCol]
  
  correlation = x.corr(y)
  
  slope = correlation*(y.std()/x.std())
  yIntercept=y.mean()- x.mean()*slope
  
  return slope, yIntercept

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
  

import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# df =df.loc[df['Cases']!=0]
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
def createPolyReg(df, xCol, yCol,file_name,order=1,save =True,color= 'Blue'):
  transformer = PolynomialFeatures(degree=order)
  X = transformer.fit_transform(df[[xCol]].values)

  clf = LinearRegression(fit_intercept=False)
  clf.fit(X, df[yCol])
  if('All' in file_name):
    sns.lmplot(
      data=df,
      x=xCol,
      y=yCol,
      fit_reg= False,
      hue= 'Borough',
      scatter_kws={'alpha':0.5}
    )
  else:
    sns.regplot(
      data=df,
      x=xCol,
      y=yCol,
      x_jitter=500,
      color= color,
      scatter_kws={'alpha':0.5}
    )
  xs = np.linspace(0,50000).reshape(-1, 1)
  ys = clf.predict(transformer.transform(xs))
  plt.ylim(30,150)
  
  plt.plot(xs, ys)
  plt.title(f'Covid Cases vs Attendance Rate (Degree {order})')
  
  vals = np.arange(0,len(df)).reshape(-1, 1)
  expected= clf.predict(transformer.transform(vals))
  
  mse =round(mean_squared_error(df[yCol],expected),4)
  mae =round(mean_absolute_error(df[yCol],expected),4)
  
  slope, intercept = computeLinearReg(df, xCol, yCol)
  plt.text(
    5000,60,
    f'Mean Squared Error: {mse}'+
    f'\nMean Absolute Error: {mae}'+
    f'\nLinear:\nSlope: {round(slope,4)}\nY-Intercept: {round(intercept,4)}'
  )
  if(save):
    plt.savefig(
      file_name,
      bbox_inches="tight",
      dpi=300,
      transparent=True
    )
  if(not save):
    plt.show()
  plt.close()