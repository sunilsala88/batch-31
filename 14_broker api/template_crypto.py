


import pendulum as dt
import logging

from alpaca.trading.requests import GetOrdersRequest,MarketOrderRequest
from alpaca.trading.enums import OrderSide, QueryOrderStatus,TimeInForce
from alpaca.data.historical import CryptoHistoricalDataClient
from zoneinfo import ZoneInfo
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
from alpaca.data.requests import CryptoBarsRequest

from alpaca.trading.client import TradingClient

list_of_tickers=["ETH/USD",'AAVE/USD']
time_zone='America/New_York'
strategy_name='crypto_sma'


logging.basicConfig(level=logging.INFO, filename=f'{strategy_name}_{dt.now(tz=time_zone).date()}.log',filemode='a',format="%(asctime)s - %(message)s")





def sma(close, length=None, talib=None, offset=None, **kwargs):
    # Validate inputs
    if close is None or len(close) == 0:
        return None
    n = len(close)
    length = int(length) if length is not None and length > 0 else 10
    min_periods = int(kwargs["min_periods"]) if "min_periods" in kwargs and kwargs["min_periods"] is not None else length
    offset = int(offset) if offset is not None else 0

    # Precompute cumulative sums for efficient window calculations
    cumulative = [0] * (n + 1)
    for i in range(1, n + 1):
        cumulative[i] = cumulative[i - 1] + close[i - 1]  # Access list elements directly

    # Compute SMA with min_periods handling
    sma_vals = []
    for i in range(n):
        start_idx = max(0, i - length + 1)
        window_length = i - start_idx + 1
        
        if window_length < min_periods:
            sma_vals.append(None)
        else:
            window_sum = cumulative[i + 1] - cumulative[start_idx]
            sma_vals.append(window_sum / window_length)

    # Apply offset shifting
    if offset > 0:
        sma_vals = [None] * offset + sma_vals
        sma_vals = sma_vals[:n]  # Maintain original length
    elif offset < 0:
        offset_abs = abs(offset)
        sma_vals = sma_vals[offset_abs:] + [None] * offset_abs

    # Handle fillna
    if "fillna" in kwargs:
        fill_val = kwargs["fillna"]
        sma_vals = [fill_val if x is None else x for x in sma_vals]

    # Handle fill_method
    if "fill_method" in kwargs:
        method = kwargs["fill_method"]
        if method == "ffill":
            last_val = None
            for i in range(n):
                if sma_vals[i] is not None:
                    last_val = sma_vals[i]
                elif last_val is not None:
                    sma_vals[i] = last_val
        elif method == "bfill":
            next_val = None
            for i in range(n - 1, -1, -1):
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

    return sdata

ticker=list_of_tickers[0]
data= get_historical_crypto_data(ticker,30,TimeFrameUnit.Minute)
print(data)

print('strategy started')
logging.info('strategy started')