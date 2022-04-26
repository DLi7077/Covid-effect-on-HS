import pandas as pd

def computeLinearReg(df:pd.DataFrame,xCol,yCol):
  x= df[xCol]
  y= df[yCol]
  
  correlation = x.corr(y)
  
  slope = correlation*(y.std()/x.std())
  yIntercept=y.mean()- x.mean()*slope
  
  return slope, yIntercept