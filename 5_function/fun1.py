


# def average(list1):
#     total=0
#     for i in list1:
#         total=total+i
#     avg=total/len(list1)
#     return avg

# list1=[33,44,55,66]
# a=average(list1)
# print(a)

# prices=[55,43,2]
# b=average(prices)
# print(b)


#parameter
#argument

def square(num1):
    s=5**2
    print(s)
    return num1

a=square(10)
print(a)



num_fib=10
fib1=0
fib2=1

for i in range(num_fib-2):
    current_fib=fib1+fib2
    print(current_fib)
    fib1=fib2
    fib2=current_fib

#fibonacci
#return list of n fibb number