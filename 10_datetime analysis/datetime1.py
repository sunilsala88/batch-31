d1='2025-01-01'
import datetime as dt
d1=dt.datetime(2025,1,1,11,55,30)
d2=dt.date(2025,1,1)
d3=dt.time(11,55,30)
print(d1)
print(d2)
print(d3)
print(d1)

t1=dt.timedelta(days=1)
print(d1+t1)
print(d1.weekday())
#create a list of all dates in 2025
#create a list of all thursday in 2025