#type 3 
#when you use index to acces the list

stocks=['amzn','tsla','ongc','reliance','goog',33,44,55]


for i in range(len(stocks)):
    print(stocks[i])


stocks=['amzn','tsla','ongc','reliance','goog']
prices=[555,333,667,345,678]

stock_prices={}


for i in range(len(stocks)):
    stock_prices.update({stocks[i]:prices[i]})


print(stock_prices)