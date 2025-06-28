

from backtesting import Backtest,Strategy
import yfinance as yf
import pandas as pd

#yfinance
data=yf.download('AMZN',period='max',multi_level_index=False)
print(data)

#from csv
data=pd.read_csv('/Users/algo trading 2025/batch 31/15_backtesting/data.csv')
data=data[['timestamp','open','high','low','close','volume']]
data=data.rename(columns={'timestamp':'Date','open':'Open','high':"High",'low':'Low','close':'Close','volume':"Volume"})
data['Date']=pd.to_datetime(data['Date'])
data['Date']=data['Date'].dt.tz_localize(None)
data.set_index('Date',inplace=True)
data=data.iloc[:3000]


class Bollinger(Strategy):

    def init(self):
        pass

    def next(self):
        pass

bt=Backtest(data,Bollinger,cash=10_000)
output=bt.run()
print(output)
bt.plot()