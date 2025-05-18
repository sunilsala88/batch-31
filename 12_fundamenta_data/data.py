

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