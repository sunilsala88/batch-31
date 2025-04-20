
# import file1

# print(file1.a)
# print(file1.get_number())

# b1=file1.Broker('jay',123,1000)



import file1 as f1

print(f1.a)
print(f1.get_number())

b1=f1.Broker('jay',123,1000)


from file1 import get_number
print(get_number())

import new.file3 as f3
print(f3.b)


#module package library

import random
import time
import os
import sys

import datetime
print(datetime.datetime.now())

print(os.getcwd())

num=13
if num==12:
    sys.exit()

print(random.randint(100,200))
time.sleep(1)
print(time.time())
