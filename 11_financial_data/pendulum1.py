#pip install pendulum

import pendulum as dt

time_zone='Asia/Kolkata'

def main():
    print('strategy started')
    print(dt.now(tz=time_zone))

start=dt.time(19,58)
end=dt.time(20,1)
import time
while dt.now(tz=time_zone).time()<end:
    print(dt.now(tz=time_zone))
    if dt.now(tz=time_zone).second==1:
        main()
    time.sleep(1)