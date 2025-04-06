
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

v=reverse_string('tsla')
print(v)


stock_prices={'amzn': 555, 'tsla': 333, 'ongc': 667, 'reliance': 345, 'goog': 678}

for i,j in stock_prices.items():
    print(i,":",j)

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

print(portfolio)