
l1=[22,33,44,55,66]
print(l1)
print(l1[:2])

l1.append(66)
l1.append(99)
print(l1)
l1.insert(2,58)
print(l1)

l1.remove(66)
print(l1)
l1.pop(0)
print(l1)

del l1[-1]
print(l1)

l1[0]=44
print(l1)

s1='hello'
s1=s1.replace('l','a')
s1.index('e')