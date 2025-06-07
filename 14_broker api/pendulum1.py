

time_zone1="America/New_York"
time_zone2='Asia/Kolkata'
time_zone3='UTC'
import datetime as dt
import pytz

tz1=pytz.timezone(time_zone3)
print(dt.datetime.now(tz=tz1))

import pendulum as dt
print(dt.now(time_zone3))