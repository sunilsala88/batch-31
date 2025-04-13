
def reverse_string(s:str)-> str:
    """
    this will reverse the string
    """
    string1=s
    new_string=""
    index1=-1
    while True:
        new_string=new_string+string1[index1]

        if index1==len(string1)*(-1):
            break
        index1=index1-1
    return new_string

# v=reverse_string('tsla')
# print(v)




def print_stock_prices():

    for i,j in stock_prices.items():
        print(i,":",j)



def get_portfolio():
    portfolio=[]

    while True:
        stock_name=input('enter the stock name (press q to quit)')
        print(stock_name)

        if stock_name.upper()=='Q':
            break

        if stock_name=='ongc':
            print('we cannot trade this stock')
            continue

        found=stock_prices.get(stock_name)
        if found:
            portfolio.append(stock_name)
        else:
            print('stock does not exist')

    return (portfolio)


# stock_prices={'amzn': 555, 'tsla': 333, 'ongc': 667, 'reliance': 345, 'goog': 678}
# print_stock_prices()
# s=get_portfolio()
# print(s)

def fun1(num1):
    # global temp
    temp=4
    a=num1*temp
    return a

def fun2(num3,num4):
    m=num3*num4
    return m

temp=2

a=fun1(10)
b=fun2(20,30)
print(a,b)
print(temp)


def double_money(money:int , inter=6)-> int:
    """
    this function will tell you how many years it will take to double your investment
    """

    money=money
    initial_money=money
    annual_ret=inter
    years=0

    while True:
        if money>2*initial_money:
            break
        money=money+(money*(annual_ret/100))
        years=years+1

    return (years)

y=double_money(1000)
print(y)


def get_intro(name:str,age:int)->str:
    """
    return a intro
    """
    # intro="my name is "+name+' and my age is '+ str(age)
    intro=f"my name is {name} and my age is {age}"

    return intro

i=get_intro('vishal',30)
print(i)

#what is fstring


#keyword argument

def student(firstname, lastname):
    print(firstname, lastname)

student(firstname="John", lastname="Doe")
student(lastname="Doe", firstname="John")


def get_vwap(prices:list,volumes:list)->int:
    """
    calculates vwap for the give list of volume and prices
    """
    Prices=prices
    Volumes=volumes

    sum_of_mul=0
    sum_of_vol=0
    for i in range(len(Prices)):
        p,v=Prices[i],Volumes[i]
        sum_of_mul=sum_of_mul+p*v
        sum_of_vol=sum_of_vol+v

    return (sum_of_mul/sum_of_vol)

v=get_vwap([12,3,4,6],[55,66,77,88])
print(v)





# def power(x):
#     return x**2

# power = lambda x: x * 2

# x=2
# n=power(2)
# print(n)




def modify_value(x):
    x = 10

num = 5
modify_value(num)
print(num)

def modify_list(lst):
    lst.append(4)

my_list = [1, 2, 3]
modify_list(my_list)
print(my_list)

def modify_list(lst):
    lst.update({3:4})

my_list = {1:2}
modify_list(my_list)
print(my_list)