

from backtesting import Backtest,Strategy
import yfinance as yf
import pandas as pd

# #yfinance
# data=yf.download('AMZN',period='max',multi_level_index=False)
# print(data)

#from csv
data=pd.read_csv('/Users/algo trading 2025/batch 31/15_backtesting/data.csv')
data=data[['timestamp','open','high','low','close','volume']]
data=data.rename(columns={'timestamp':'Date','open':'Open','high':"High",'low':'Low','close':'Close','volume':"Volume"})
data['Date']=pd.to_datetime(data['Date'])
data['Date']=data['Date'].dt.tz_localize(None)
data.set_index('Date',inplace=True)
data=data.iloc[:1000]

import talib

def upper(close,length):
    u,m,l=talib.BBANDS(close,length)
    return u

def lower(close,length):
    u,m,l=talib.BBANDS(close,length)
    return l

class Bollinger(Strategy):
    l=10
    def init(self):
        self.upper1=self.I(upper,self.data.Close.s,self.l)
        self.lower1=self.I(lower,self.data.Close.s,self.l)

    def next(self):
        
        # if self.data.Close[-1]<self.lower1[-1] and not self.position:
        #     # self.position.close()
        #     self.buy()
        # elif self.data.Close[-1]>self.upper1[-1] and self.position:
        #     self.position.close()


        if self.data.Close[-1]<self.lower1[-1] and ((not self.position) or (self.position.is_short)):
            self.position.close()
            self.buy()
        elif self.data.Close[-1]>self.upper1[-1] and ((not self.position) or (self.position.is_long)):
            self.position.close()
            self.sell()


print(upper(data['Close'],10))
print(lower(data['Close'],10))

bt=Backtest(data,Bollinger,cash=10_000)
output=bt.run()
print(output)
bt.plot()