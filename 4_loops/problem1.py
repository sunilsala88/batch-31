

#fibonacci number
#0,1,1,2,3,5,8,13,21,34

num_fib=10
fib1=0
fib2=1

for i in range(num_fib-2):
    current_fib=fib1+fib2
    print(current_fib)
    fib1=fib2
    fib2=current_fib


