


import pendulum as dt
import logging
import time
import pandas as pd

from alpaca.trading.requests import GetOrdersRequest,MarketOrderRequest
from alpaca.trading.enums import OrderSide, QueryOrderStatus,TimeInForce
from alpaca.data.historical import CryptoHistoricalDataClient
from zoneinfo import ZoneInfo
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
from alpaca.data.requests import CryptoBarsRequest

from alpaca.trading.client import TradingClient

list_of_tickers=["ETH/USD",'AAVE/USD','SOL/USD']
time_zone='America/New_York'
strategy_name='crypto_sma'


logging.basicConfig(level=logging.INFO, filename=f'{strategy_name}_{dt.now(tz=time_zone).date()}.log',filemode='a',format="%(asctime)s - %(message)s")

from alpaca.trading.client import TradingClient
api_key='PKCGQ99MC5FQA1P8ZSRE'
secret_key='rkWLI1F2poiTbuERdzozfOLgVV6mrFKTH27Ugvb1'
trading_client = TradingClient(api_key, secret_key, paper=True)

import talib
import pandas_ta as ta

def sma(close, length=None, talib=None, offset=None, **kwargs):
    # Convert input to list to avoid pandas indexing issues
    if close is None:
        return None
    
    try:
        # Convert any iterable to list (pandas Series, tuple, numpy array, etc.)
        close = list(close)
    except TypeError:
        raise TypeError("close must be an iterable")
    
    n = len(close)
    if n == 0:
        return None

    # Validate parameters
    length = int(length) if length is not None and length > 0 else 10
    min_periods = int(kwargs["min_periods"]) if "min_periods" in kwargs and kwargs["min_periods"] is not None else length
    offset = int(offset) if offset is not None else 0

    # Precompute cumulative sums for efficient SMA calculation
    cumulative = [0] * (n + 1)
    for i in range(1, n + 1):
        cumulative[i] = cumulative[i - 1] + close[i - 1]

    # Calculate SMA with min_periods handling
    sma_vals = []
    for i in range(n):
        start_idx = max(0, i - length + 1)
        window_length = i - start_idx + 1
        
        if window_length < min_periods:
            sma_vals.append(None)
        else:
            window_sum = cumulative[i + 1] - cumulative[start_idx]
            sma_vals.append(window_sum / window_length)

    # Apply offset
    if offset > 0:
        sma_vals = [None] * offset + sma_vals[:n-offset]
    elif offset < 0:
        offset_abs = abs(offset)
        sma_vals = sma_vals[offset_abs:] + [None] * min(offset_abs, n)

    # Handle fillna
    if "fillna" in kwargs:
        fill_val = kwargs["fillna"]
        sma_vals = [fill_val if x is None else x for x in sma_vals]

    # Handle fill methods
    if "fill_method" in kwargs:
        method = kwargs["fill_method"]
        n = len(sma_vals)
        
        if method == "ffill":
            last_val = None
            for i in range(n):
                if sma_vals[i] is not None:
                    last_val = sma_vals[i]
                elif last_val is not None:
                    sma_vals[i] = last_val
        
        if method == "bfill":
            next_val = None
            for i in range(n-1, -1, -1):
                if sma_vals[i] is not None:
                    next_val = sma_vals[i]
                elif next_val is not None:
                    sma_vals[i] = next_val

    return sma_vals

def get_historical_crypto_data(ticker,duration,time_frame_unit):
    # setup crypto historical data client
    crypto_historical_data_client = CryptoHistoricalDataClient()
    """extracts historical data and outputs in the form of dataframe"""
    # now = datetime.now(ZoneInfo("America/New_York"))
    now=dt.now(tz=time_zone)
    req = CryptoBarsRequest(
        symbol_or_symbols = ticker,
        timeframe=TimeFrame(amount = 1, unit = time_frame_unit), # specify timeframe
        # start = now - timedelta(days = duration),                          # specify start datetime, default=the beginning of the current day.
        start=now-dt.duration(days=duration)
        # end_date=None,                                        # specify end datetime, default=now
        # limit = 2,                                               # specify limit
    )
    history_df1=crypto_historical_data_client.get_crypto_bars(req).df
    sdata=history_df1.reset_index().drop('symbol',axis=1)
    sdata['timestamp']=sdata['timestamp'].dt.tz_convert('America/New_York')
    sdata=sdata.set_index('timestamp')
    sdata['sma_20']=sma(sdata['close'],length=20)
    sdata['sma_50']=sma(sdata['close'],length=50)
    sdata['atr']=talib.ATR(sdata['high'],sdata['low'],sdata['close'],14)

    return sdata

ticker=list_of_tickers[0]
data= get_historical_crypto_data(ticker,30,TimeFrameUnit.Minute)
print(data)

print('strategy started')
logging.info('strategy started')

def get_all_open_orders():
    # params to filter orders by
    request_params = GetOrdersRequest(
                        status=QueryOrderStatus.OPEN
                    )

    # orders that satisfy params
    orders = trading_client.get_orders(filter=request_params)
    new_order=[]
    for elem in orders:
        new_order.append(dict(elem))

    order_df=pd.DataFrame(new_order)
    
    l=[i for i in list_of_tickers]
    order_df=order_df[order_df['symbol'].isin(l)]
    order_df.to_csv('orders1.csv')
    return order_df

def get_all_position():

    pos=trading_client.get_all_positions()
    new_pos=[]
    for elem in pos:
        new_pos.append(dict(elem))

    pos_df=pd.DataFrame(new_pos)
    # print(pos_df)
    # filter pos that are in list_of_tickers
    l=[i.replace("/","") for i in list_of_tickers]
    pos_df=pos_df[pos_df['symbol'].str.replace('/','').isin(l)]
    pos_df.to_csv('position1.csv')
    return pos_df

def trade_buy_stocks(ticker,closing_price):
    print('placing market order')
    # preparing orders
    market_order_data = MarketOrderRequest(
                        symbol=ticker,
                        qty=1,
                        side=OrderSide.BUY,
                        time_in_force=TimeInForce.GTC
                        )

    # Market order
    market_order = trading_client.submit_order(
                    order_data=market_order_data
                )
    print(market_order)
    print('done placing market order for ',ticker)

def strategy(hist_df,ticker):
    print('inside strategy conditional code ')
    # print(hist_df)
    print(ticker)
    buy_condition=(hist_df['sma_20'].iloc[-1]>hist_df['sma_50'].iloc[-1]) and (hist_df['sma_20'].iloc[-2]<hist_df['sma_50'].iloc[-2])
    # buy_condition=True
    money=float(trading_client.get_account().cash)
    money=money/3
    print(money)
    closing_price=hist_df['close'].iloc[-1]
    if money>closing_price:
        if buy_condition:
            print('buy condition satisfied')
            trade_buy_stocks(ticker,closing_price)
        else:
            print('no condition satisfied')
    else:
        print('we dont have enough money to trade')

def main_strategy_code():
    logging.info('we are running strategy ')
    ord_df=get_all_open_orders()
    pos_df=get_all_position()
    print(ord_df)
    print(pos_df)

    for ticker in list_of_tickers:
        print(ticker)
        #fetch historical data and indicators
        hist_df=get_historical_crypto_data(ticker,2,TimeFrameUnit.Minute)
        print(hist_df)

        money=float(trading_client.get_account().cash)
        money=money/3
        print(money)
        ltp=hist_df['close'].iloc[-1]
        print(ltp)
        quantity=money//ltp
        print(quantity)


        if quantity==0:
            continue
        
        if pos_df.empty:
            print('we dont have any position')
            strategy(hist_df,ticker)

current_time=dt.now(tz=time_zone)
print(current_time)

start_hour,start_min=9,36
end_hour,end_min=9,50

start_time=dt.datetime(current_time.year,current_time.month,current_time.day,start_hour,start_min,tz=time_zone)
end_time=dt.datetime(current_time.year,current_time.month,current_time.day,end_hour,end_min,tz=time_zone)

print(start_time)
print(end_time)


#this code will execute before the start time
while dt.now(tz=time_zone)<start_time:
    print(dt.now(tz=time_zone))
    time.sleep(1)
print('we have reached start time')



while True:
    if dt.now(tz=time_zone)>end_time:
        break
    ct=dt.now(tz=time_zone)
    print(ct)
    
    if ct.second==1: #and ct.minute in range(0,60,5):#[0,5,10,15..55]
        main_strategy_code()
    time.sleep(1)
print('strategy stopped')