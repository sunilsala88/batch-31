#get ohlc daily data from alpaca

import yfinance as yf

# Get the data for the stock AAPL
data = yf.download('AAPL','2016-01-03','2023-12-01',multi_level_index=False)
print(data)
data.to_csv('AAPL_history.csv')