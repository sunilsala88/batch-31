
import pandas as pd

#convert string to datetime
s='2025-01-01 11:55:30'
t1=pd.to_datetime(s)
print(t1)

#datetime to string
f='%b %A %Y'
print(t1.strftime(f))

#adding unit time
print(t1+pd.Timedelta(365,unit='D'))

#datetime to epoch
print(t1.timestamp())

#epoch to datetime
n=1735732530
d2=pd.to_datetime(n,unit='s')
print(d2)

