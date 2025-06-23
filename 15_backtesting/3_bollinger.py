from backtesting import Backtest, Strategy
# import indicators as ta
import talib 

def upper1(close,length):
    upper,middle,lower=talib.BBANDS(close,length)
    return upper

def lower1(close,length):
    upper,middle,lower=talib.BBANDS(close,length)
    return lower

class Bollinger_s(Strategy):
    n1 = 10


    def init(self):
        close = self.data.Close.s
        self.upper = self.I(upper1, close, self.n1)
        self.lower = self.I(lower1, close, self.n1)


    def next(self):
        close_price=self.data.Close[-1]
        current_upper=self.upper[-1]
        current_lower=self.lower[-1]
        if close_price<current_lower:
            self.position.close()
            self.buy()
        elif close_price>current_upper:
            self.position.close()
            self.sell()




import yfinance as yf
data=yf.download('MSFT',period='max',interval='1m',multi_level_index=False)
print(data)

upper,middle,lower=talib.BBANDS(data['Close'],10)

bt = Backtest(data, Bollinger_s,
              cash=10000, commission=.002,
              exclusive_orders=True,trade_on_close=True)

output = bt.run()
bt.plot()
print(output)

output['_trades'].to_csv('trades.csv')