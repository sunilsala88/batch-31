
stock_prices={'amzn': 555, 'tsla': 333, 'ongc': 667, 'reliance': 345, 'goog': 678}

def print_stocks():
    for i,j in stock_prices.items():
        print(i,":",j)

def get_portfoilio():
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

print_stocks()
p=get_portfoilio()
print(p)