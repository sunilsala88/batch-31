

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

#iterable


string1='fessorpro'
for i in string1:
    print(i)

a=(44,55,66)
for i in a:
    print(i)


Prices=[100, 105, 110]
Volumes=[200, 150, 300]

sum_of_mul=0
sum_of_vol=0
for i in range(len(Prices)):
    p,v=Prices[i],Volumes[i]
    sum_of_mul=sum_of_mul+p*v
    sum_of_vol=sum_of_vol+v

print(sum_of_mul/sum_of_vol)