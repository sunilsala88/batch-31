
import yfinance as yf
import pandas as pd
stock_name='TSLA'
y1=yf.Ticker(stock_name)
print(y1)

#incom
print(y1.incomestmt)

#bal
print(y1.quarterly_balance_sheet)

#cash
print(y1.get_cash_flow())