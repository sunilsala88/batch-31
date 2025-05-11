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

# l1=[]
# dt1=dt.datetime(2025,1,1)
# for i in range(1,366):
#     dt1=dt1+dt.timedelta(days=1)
#     if dt1.weekday()==3:

#         l1.append(dt1)
# print(l1)


current_time=dt.datetime.now()
print(current_time)

#timestamp (epoch time)
num=1746968116+60
dt1=dt.datetime.fromtimestamp(num)
print(dt1)

#datetime object to epoch
print(dt1.timestamp())

#convert string to datetime

s1='2025-29-05'
f='%Y-%d-%m'
d4=dt.datetime.strptime(s1,f)
print(d4)
#https://www.programiz.com/python-programming/datetime/strftime

a='12/24/2018, 04:59:31'
f='%m/%d/%Y, %H:%M:%S'
d5=dt.datetime.strptime(a,f)
print(d5)

#convert datetime to string
f='%b %A %Y'
s=d5.strftime(f)
print(s)