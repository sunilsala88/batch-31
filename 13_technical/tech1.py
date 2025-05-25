import yfinance as yf
import pandas as pd

stock_name = 'TSLA'
df = yf.download(stock_name,multi_level_index=False,period='12mo')
print(df)

import mplfinance as mpf
import pandas_ta as ta
# ema1=ta.ema(df['Close'])
# df['sma']=ta.sma(df['Close'])
import talib as ta1
ema1=ta1.EMA(df['Close'])
df['sma']=ta1.SMA(df['Close'])


a=mpf.make_addplot(ema1,color='black')
b=mpf.make_addplot(df['sma'],color='blue')
mpf.plot(df,type='candle',style='yahoo',addplot=[a,b])