
f=open('sample.txt','r')
data=f.read()
l=data.split()
print(len(l))
f.close()