from backtesting import Backtest, Strategy
# import indicators as ta
import talib 

def get_sma(closing_price,length):
    return talib.SMA(closing_price,length)

class SmaCross(Strategy):
    n1 = 30
    n2 = 50

    def init(self):
        close = self.data.Close.s
        self.sma1 = self.I(get_sma, close, self.n1)
        self.sma2 = self.I(get_sma, close, self.n2)


    def next(self):
        if self.sma1[-1]<self.sma2[-1] and self.sma1[-2]>self.sma2[-2]:
            self.position.close()
            self.buy()
        elif self.sma1[-1]>self.sma2[-1] and self.sma1[-2]<self.sma2[-2]:
            self.position.close()
            self.sell()

import yfinance as yf
data=yf.download('MSFT',period='max',interval='1m',multi_level_index=False)
print(data)


bt = Backtest(data, SmaCross,
              cash=10000, commission=.002,
              exclusive_orders=True,trade_on_close=True)

output = bt.run()
bt.plot()
print(output)

output['_trades'].to_csv('trades.csv')