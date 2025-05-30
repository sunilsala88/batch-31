
stock_prices={'amzn': 555, 'tsla': 333, 'ongc': 667, 'reliance': 345, 'goog': 678}

def print_stocks():
    for i,j in stock_prices.items():
        print(i,":",j)

def get_portfoilio():
    portfolio={}

    while True:
        stock_name=input('enter the stock name (press q to quit)')
        print(stock_name)

        if stock_name.upper()=='Q':
            break

        if stock_name=='ongc':
            print('we cannot trade this stock')
            continue

        found=stock_prices[stock_name]
        if found:
            portfolio.update({stock_name:found})
        else:
            print('stock does not exist')

    return (portfolio)



def save_data(p)->None:
    f=open('data.txt','w')
    total=0
    for stock,price in p.items():
        sent=f"{stock}:{price}\n"
        total=total+price
        f.write(sent)
    sent=f"total:{total}\n"
    f.write(sent)
    f.close()

print_stocks()
p=get_portfoilio()
print(p)
save_data(p)