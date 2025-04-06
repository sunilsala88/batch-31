


def average(list1):
    total=0
    for i in list1:
        total=total+i
    avg=total/len(list1)
    return avg

list1=[33,44,55,66]
a=average(list1)
print(a)

prices=[55,43,2]
b=average(prices)
print(b)