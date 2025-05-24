import yfinance as yf
import pandas as pd

stock_name = 'TSLA'
df = yf.download(stock_name)
print(df)
