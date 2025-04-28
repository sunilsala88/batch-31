import numpy as np
# l1=[1,2,3.5,'hello']
# r1=np.array(l1)
# print(l1)
# print(r1)

# l1=[1,2,3]
# l2=[4,5,'6']

# np1=np.array(l1)
# np2=np.array(l2)

# # print(l1+3)
# print(np1*10)

# print(list(range(1,10)))
# print(np.arange(1,10))
# print(np.zeros(10))
# print(np.ones(10))

l3=[[1,2,3],[4,5,6],[7,8,9]]
np3=np.array(l3)
print(l3)
print(np3)

#indexing
print(np3[2,1])
#sling
print(np3[0,:])

print(np.arange(25).reshape(5,5))
print(np.random.randint(100,200,25).reshape(5,5))

# import datetime as dt
# print(dt.datetime.now())
# import datetime
# print(datetime.datetime.now())
# from datetime import datetime
# print(datetime.now())