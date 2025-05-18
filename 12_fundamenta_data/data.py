

# tickers=[
#     'TSLA',"AMZN","GOOG"
# ]

# import yfinance as yf

# data=yf.download(tickers)
# print(data['Close'])

# data={}
# for i in tickers:
#     v=yf.download(i,multi_level_index=False)
#     data.update({i:v})
# print(data)

import yfinance as yf
import pandas as pd
stock_name='TSLA'
y1=yf.Ticker(stock_name)
print(y1)

# print(y1.get_info())
# print(y1.info)

data=pd.Series(y1.info)
print(data)
data.to_csv('data.csv')

symbols=['TSLA',"GOOG",'MSFT',"AAPL",'NVDA']
mark_cap=[]

for i in symbols:
    b=yf.Ticker(i).get_info()
    mark_cap.append(b.get('marketCap'))

print(mark_cap)
for i in range(len(symbols)):
    print(symbols[i],mark_cap[i])

max=mark_cap[0]
name=''
for i in range(len(mark_cap)):
    if max<mark_cap[i]:
        max=mark_cap[i]
        name=symbols[i]
print('\n')
print(name,max)

