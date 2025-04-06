


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


def get_fibonacci(num):
    num_fib=num
    fib_numbers=[0,1]
    fib1=fib_numbers[0]
    fib2=fib_numbers[1]

    for i in range(num_fib-2):
        current_fib=fib1+fib2
        fib_numbers.append(current_fib)
        fib1=fib2
        fib2=current_fib
    return fib_numbers

# f=get_fibonacci(100)
# print(f)
#fibonacci
#return list of n fibb number

#positional parameter
def power(num1,num2):
    a=num1**num2
    return a

a=5
b=2
v=power(a,b)
print(v)


