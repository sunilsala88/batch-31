
def reverse_string(s):
    string1=s
    new_string=""
    index1=-1
    while True:
        new_string=new_string+string1[index1]

        if index1==len(string1)*(-1):
            break
        index1=index1-1
    # return new_string

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



money=1000
initial_money=money
annual_ret=5
years=0

while True:
    if money>2*initial_money:
        break
    money=money+(money*(annual_ret/100))
    years=years+1

print(years)
