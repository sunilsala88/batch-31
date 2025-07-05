from backtesting import Backtest, Strategy
# import indicators as ta
import talib 

def get_sma(closing_price,length):
    return talib.SMA(closing_price,length)

class SmaCross(Strategy):
    n1 = 30
    n2 = 50
    sl1=0.05

    def init(self):
        close = self.data.Close.s
        self.sma1 = self.I(get_sma, close, self.n1)
        self.sma2 = self.I(get_sma, close, self.n2)


    def next(self):
        if self.sma1[-1]<self.sma2[-1] and self.sma1[-2]>self.sma2[-2]:
            self.position.close()
            buy_price=self.data.Close[-1]
            self.buy(sl=buy_price*(1-self.sl1))
        elif self.sma1[-1]>self.sma2[-1] and self.sma1[-2]<self.sma2[-2]:
            self.position.close()
            buy_price=self.data.Close[-1]
            self.sell(sl=buy_price*(1+self.sl1))

import yfinance as yf
data=yf.download('NVDA',period='1y',interval='1h',multi_level_index=False)
print(data)


bt = Backtest(data, SmaCross,
              cash=10000, commission=.002,
              exclusive_orders=True,trade_on_close=True)

output = bt.run()
bt.plot()
print(output)


output=bt.optimize(sl1=[0.01,0.02,0.03,0.04,0.05,0.06],n1=range(25,35,2),n2=range(45,55,2),maximize='Return [%]')
print(output)
print(output['_strategy'])
bt.plot()
