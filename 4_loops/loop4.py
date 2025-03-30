stock_prices={'amzn': 555, 'tsla': 333, 'ongc': 667, 'reliance': 345, 'goog': 678}


print(list(stock_prices.keys()))
print(list(stock_prices.values()))
print(list(stock_prices.items()))

for i in stock_prices:
    print(i)
    print(stock_prices.get(i))

#type 4 loop 
for i,j in stock_prices.items():
    print(i,j)

#count positive values in a list
l1=[33,-44,-55,667,-88,74,3948,87342]

count=0
for i in l1:
    if i<0:
        count=count+1
    
print(count)