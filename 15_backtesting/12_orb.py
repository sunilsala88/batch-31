# 15-min TF
# 9.15 - 9.30

# 3 or 5 min candles closing above range of first 15-min candle

# Apply - 9/21/50 moving average logic -- if 9>21>50 go for long
# Close - if price is closing below Supertrend (10,1.5)

#5 min data
#high and low from 9:30 to 10:00
#sma_9,sma_21,sma50
#closing condition supertend -1 close
#close at 3:15



from backtesting import Backtest, Strategy

import pandas as pd
import yfinance as yf
import time
import numpy as np

import talib 

def get_sma(closing_price,length):
    return talib.SMA(closing_price,length)

def supertrend(high, low, close, length=10, multiplier=3):
    """
    Supertrend function that matches pandas_ta.supertrend output.
    
    Args:
        high (pd.Series): Series of high prices
        low (pd.Series): Series of low prices
        close (pd.Series): Series of close prices
        length (int): The ATR period. Default: 7
        multiplier (float): The ATR multiplier. Default: 3.0
    
    Returns:
        pd.DataFrame: DataFrame with columns:
            SUPERT - The trend value
            SUPERTd - The direction (1 for long, -1 for short)
            SUPERTl - The long values
            SUPERTs - The short values
    """
    # Calculate ATR using the pandas_ta method (RMA - Rolling Moving Average)
    tr1 = high - low
    tr2 = abs(high - close.shift(1))
    tr3 = abs(low - close.shift(1))
    true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = true_range.ewm(alpha=1/length, adjust=False).mean()

    # Calculate basic bands
    hl2 = (high + low) / 2
    upperband = hl2 + (multiplier * atr)
    lowerband = hl2 - (multiplier * atr)

    # Initialize direction and trend
    direction = [1]  # Start with long
    trend = [lowerband.iloc[0]]  # Start with lowerband
    long = [lowerband.iloc[0]]
    short = [np.nan]

    # Iterate through the data to calculate the Supertrend
    for i in range(1, len(close)):
        if close.iloc[i] > upperband.iloc[i - 1]:
            direction.append(1)
        elif close.iloc[i] < lowerband.iloc[i - 1]:
            direction.append(-1)
        else:
            direction.append(direction[i - 1])
            if direction[i] == 1 and lowerband.iloc[i] < lowerband.iloc[i - 1]:
                lowerband.iloc[i] = lowerband.iloc[i - 1]
            if direction[i] == -1 and upperband.iloc[i] > upperband.iloc[i - 1]:
                upperband.iloc[i] = upperband.iloc[i - 1]

        if direction[i] == 1:
            trend.append(lowerband.iloc[i])
            long.append(lowerband.iloc[i])
            short.append(np.nan)
        else:
            trend.append(upperband.iloc[i])
            long.append(np.nan)
            short.append(upperband.iloc[i])

    # Create DataFrame to return
    df = pd.DataFrame({
        "SUPERT": trend,
        "SUPERTd": direction,
        "SUPERTl": long,
        "SUPERTs": short,
    }, index=close.index)

    return df



def super1(high,low,close,l=10,m=3):
    s=supertrend(high,low,close,l,m)
    # return (s[f'SUPERT_{l}_{m}.0'])
    return s['SUPERT']

def trend(high,low,close,l=10,m=3):
    s=supertrend(high,low,close,l,m)
    # return (s[f'SUPERTd_{l}_{m}.0'])
    return s['SUPERTd']


class ORBStrategy(Strategy):
    n1=9
    n2=21
    n3=50
    l=10
    m=1.5
    def init(self):
        close = self.data.Close.s
        self.sma1 = self.I(get_sma, close, self.n1)
        self.sma2 = self.I(get_sma, close, self.n2)
        self.sma3 = self.I(get_sma, close, self.n3)
        self.super=self.I(super1,self.data.High.s,self.data.Low.s,self.data.Close.s,self.l,self.m)
        self.trend=self.I(trend,self.data.High.s,self.data.Low.s,self.data.Close.s,self.l,self.m)
        self.orb_high = None
        self.orb_low = None
        self.trade=0


    def next(self):
        # print(self.data.index[-1].time())
        # print(pd.Timestamp('10:00').time())

        if self.data.index[-1].time() == pd.Timestamp('10:00').time():
            print('inside')
            df=self.data.df
            # print(df)
            d=self.data.index[-1]
            d=pd.to_datetime(d.date())
            df=df[df.index>=d]
            self.orb_high = df.High.max()
            self.orb_low = df.Low.min()
            self.trade=0
            print(self.orb_high, self.orb_low,self.data.index[-1].time())

    
        if not self.position and self.orb_high and self.orb_low:
            # print('inside condition')
            if (self.data.Close[-1] > self.orb_high) and self.trade==0 and (self.sma1[-1]>self.sma2[-1]>self.sma3[-1]):
                print('buy condition satisfied')
                print(self.orb_high, self.orb_low,self.data.index[-1].time())
                p=self.data.Close[-1]
                self.buy()
                self.trade=1
            # elif (self.data.Close[-1] < self.orb_low) and self.trade==0:
            #     print('sell condition satisfied')
            #     print(self.orb_high, self.orb_low,self.data.index[-1].time())
            #     self.sell(sl=self.orb_high)
            #     self.trade=1

        elif self.position:
            # Close position by the end of the day
            # print('i have some position')
            if self.trend[-1]==-1:
                self.position.close()
                self.orb_high = None
                self.orb_low = None
                self.trade=0

        if self.data.index[-1].time()> pd.Timestamp('15:20').time():
            self.position.close()
            self.orb_high = None
            self.orb_low = None
            self.trade=0

            # print(self.position)



import yfinance as yf
data=yf.download('TSLA',period='7d',interval='5m')
print(data)
data.columns=[c[0] for c in data.columns]
data.index = data.index.tz_convert('US/Eastern')
print(data)

s=supertrend(data['High'],data['Low'],data['Close'])
print(s)

data.reset_index(inplace=True)
data['Datetime']=data['Datetime'].dt.tz_localize(None)
data.set_index('Datetime',inplace=True)

print(data)
bt = Backtest(data, ORBStrategy, cash=3000, commission=.002)
stats = bt.run()
print(stats)
bt.plot()

