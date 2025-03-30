
i=0
while True:
    if i==10:
        break
    
    i=i+1
    # if i%5==0:
    #     continue
    print(i)


print('last line')

#fibonacci number
#0,1,1,2,3,5,8,13,21,34

num_fib=10
fib1=0
fib2=1
print(fib1)
print(fib2)
for i in range(num_fib-2):
    current_fib=fib1+fib2
    print(current_fib)
    fib1=fib2
    fib2=current_fib

num_fib=10
fib1=0
fib2=1
count=2
print(fib1)
print(fib2)
while True:
    if count==10:
        break
    
    current_fib=fib1+fib2
    print(current_fib)
    fib1=fib2
    fib2=current_fib

    count=count+1