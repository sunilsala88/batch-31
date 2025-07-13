
# Supertrend and EMA Strategy
# Calculate the Supertrend on daily candles.
# Calculate the EMA (Exponential Moving Average) on hourly candles.
# Go Long:When the daily Supertrend gives a long signal and the closing price is greater than the daily EMA.
# Go Short:When the daily Supertrend gives a short signal.The closing price is less than the daily EMA.

def ema(close, length=None, talib=None, offset=None, **kwargs):
    """Indicator: Exponential Moving Average (EMA)"""
    
    # Validate Arguments
    length = int(length) if length and length > 0 else 10
    adjust = kwargs.pop("adjust", False)
    sma = kwargs.pop("sma", True)
    offset = offset if offset is not None else 0
    
    # Validate close data
    if close is None:
        return None
    
    # Convert to list if needed
    if not isinstance(close, list):
        try:
            close = list(close)
        except:
            return None
    
    # Check if we have enough data
    if len(close) < length:
        return None
    
    # Calculate smoothing factor (alpha)
    alpha = 2.0 / (length + 1)
    
    # Initialize result list
    result = [None] * len(close)
    
    if sma:
        # Use SMA for the first value
        sma_value = sum(close[:length]) / length
        result[length - 1] = sma_value
        
        # Calculate EMA starting from the SMA
        for i in range(length, len(close)):
            if close[i] is not None:
                result[i] = alpha * close[i] + (1 - alpha) * result[i - 1]
    else:
        # Use first value as initial EMA
        result[0] = close[0] if close[0] is not None else 0
        
        # Calculate EMA for remaining values
        for i in range(1, len(close)):
            if close[i] is not None:
                result[i] = alpha * close[i] + (1 - alpha) * result[i - 1]
    
    # Apply offset if specified
    if offset != 0:
        if offset > 0:
            # Shift right (add None values at the beginning)
            result = [None] * offset + result[:-offset]
        else:
            # Shift left (remove values from the beginning)
            result = result[-offset:] + [None] * (-offset)
    
    # Handle fills
    if "fillna" in kwargs:
        fill_value = kwargs["fillna"]
        result = [fill_value if x is None else x for x in result]
    
    # Create a simple result object with name and category attributes
    class EMAResult:
        def __init__(self, data, name, category):
            self.data = data
            self.name = name
            self.category = category
        
        def __iter__(self):
            return iter(self.data)
        
        def __getitem__(self, key):
            return self.data[key]
        
        def __len__(self):
            return len(self.data)
        
        def __repr__(self):
            return f"EMAResult(name='{self.name}', length={len(self.data)})"
    
    # Create result object
    ema_result = EMAResult(result, f"EMA_{length}", "overlap")
    
    return ema_result


def supertrend(high, low, close, length=7, multiplier=3.0, offset=0):
    """
    Calculate Supertrend indicator without external libraries
    
    Parameters:
    high (list or pandas.Series): High prices
    low (list or pandas.Series): Low prices  
    close (list or pandas.Series): Close prices
    length (int): Period for ATR calculation (default: 7)
    multiplier (float): ATR multiplier (default: 3.0)
    offset (int): Shift the result by offset periods (default: 0)
    
    Returns:
    pandas.DataFrame: DataFrame with supertrend columns matching original format
    """
    
    def true_range(high, low, close, i):
        """Calculate True Range for a single period"""
        if i == 0:
            return high[i] - low[i]
        
        hl = high[i] - low[i]
        hc = abs(high[i] - close[i-1])
        lc = abs(low[i] - close[i-1])
        
        return max(hl, hc, lc)
    
    def atr(high, low, close, length):
        """Calculate Average True Range"""
        if len(high) < length:
            return [0] * len(high)
        
        atr_values = []
        
        # Calculate initial ATR using simple average
        tr_sum = 0
        for i in range(length):
            tr_sum += true_range(high, low, close, i)
        
        initial_atr = tr_sum / length
        atr_values.extend([0] * (length - 1))
        atr_values.append(initial_atr)
        
        # Calculate subsequent ATR values using smoothed average
        for i in range(length, len(high)):
            tr = true_range(high, low, close, i)
            smoothed_atr = (atr_values[-1] * (length - 1) + tr) / length
            atr_values.append(smoothed_atr)
        
        return atr_values
    
    def hl2(high, low):
        """Calculate HL2 (median price)"""
        return [(h + l) / 2 for h, l in zip(high, low)]
    
    # Handle pandas Series or convert lists to have index
    try:
        # Try to use pandas if available
        import pandas as pd
        
        # Convert to pandas Series if they're lists
        if isinstance(high, list):
            high = pd.Series(high)
        if isinstance(low, list):
            low = pd.Series(low)
        if isinstance(close, list):
            close = pd.Series(close)
            
        # Validate inputs
        if not all(len(arr) == len(high) for arr in [low, close]):
            raise ValueError("All input arrays must have the same length")
        
        if len(high) < length:
            raise ValueError(f"Not enough data points. Need at least {length} periods")
            
        # Get the index for the final DataFrame
        index = close.index
        
        # Convert to lists for processing
        high_list = high.tolist()
        low_list = low.tolist()
        close_list = close.tolist()
        
    except ImportError:
        # Fallback: create simple DataFrame-like structure
        class SimpleDataFrame:
            def __init__(self, data, index=None):
                self.data = data
                self.index = index or list(range(len(list(data.values())[0])))
                self.name = None
                self.category = None
                
            def shift(self, periods):
                if periods == 0:
                    return self
                shifted_data = {}
                for col, values in self.data.items():
                    if periods > 0:
                        shifted_values = [None] * periods + values[:-periods]
                    else:
                        shifted_values = values[-periods:] + [None] * (-periods)
                    shifted_data[col] = shifted_values
                return SimpleDataFrame(shifted_data, self.index)
            
            def fillna(self, value, inplace=False):
                filled_data = {}
                for col, values in self.data.items():
                    filled_values = [value if v is None else v for v in values]
                    filled_data[col] = filled_values
                if inplace:
                    self.data = filled_data
                else:
                    return SimpleDataFrame(filled_data, self.index)
        
        # Use lists directly
        high_list = list(high) if hasattr(high, '__iter__') else high
        low_list = list(low) if hasattr(low, '__iter__') else low
        close_list = list(close) if hasattr(close, '__iter__') else close
        
        # Validate inputs
        if not all(len(arr) == len(high_list) for arr in [low_list, close_list]):
            raise ValueError("All input arrays must have the same length")
        
        if len(high_list) < length:
            raise ValueError(f"Not enough data points. Need at least {length} periods")
        
        index = list(range(len(high_list)))
        pd = None
    
    # Calculate components
    m = len(close_list)
    hl2_values = hl2(high_list, low_list)
    atr_values = atr(high_list, low_list, close_list, length)
    
    # Calculate bands
    upperband = [hl2_values[i] + multiplier * atr_values[i] for i in range(m)]
    lowerband = [hl2_values[i] - multiplier * atr_values[i] for i in range(m)]
    
    # Initialize direction and trend arrays
    direction = [1] * m
    trend = [0] * m
    supertrend_long = [float('nan')] * m
    supertrend_short = [float('nan')] * m
    
    # Calculate Supertrend
    for i in range(1, m):
        # Determine direction
        if close_list[i] > upperband[i - 1]:
            direction[i] = 1
        elif close_list[i] < lowerband[i - 1]:
            direction[i] = -1
        else:
            direction[i] = direction[i - 1]
            
            # Adjust bands based on direction
            if direction[i] > 0 and lowerband[i] < lowerband[i - 1]:
                lowerband[i] = lowerband[i - 1]
            if direction[i] < 0 and upperband[i] > upperband[i - 1]:
                upperband[i] = upperband[i - 1]
        
        # Set trend value based on direction
        if direction[i] > 0:
            trend[i] = lowerband[i]
            supertrend_long[i] = lowerband[i]
        else:
            trend[i] = upperband[i]
            supertrend_short[i] = upperband[i]
    
    # Create DataFrame with proper naming convention
    _props = f"_{length}_{multiplier}"
    
    data = {
        f"SUPERT{_props}": trend,
        f"SUPERTd{_props}": direction,
        f"SUPERTl{_props}": supertrend_long,
        f"SUPERTs{_props}": supertrend_short,
    }
    
    # Create DataFrame
    if pd is not None:
        df = pd.DataFrame(data, index=index)
    else:
        df = SimpleDataFrame(data, index)
    
    df.name = f"SUPERT{_props}"
    df.category = "overlap"
    
    # Apply offset if needed
    if offset != 0:
        df = df.shift(offset)
    
    return df


# # Example usage:
# if __name__ == "__main__":
#     # Sample data
#     high_prices = [100, 102, 105, 103, 107, 109, 108, 110, 112, 111, 113, 115]
#     low_prices = [98, 100, 103, 101, 105, 107, 106, 108, 110, 109, 111, 113]
#     close_prices = [99, 101, 104, 102, 106, 108, 107, 109, 111, 110, 112, 114]
    
#     # Calculate Supertrend
#     result = supertrend(high_prices, low_prices, close_prices, length=7, multiplier=3.0)
    
#     # Display results
#     print("Supertrend Results:")
#     print(f"DataFrame name: {result.name}")
#     print(f"DataFrame category: {result.category}")
#     print("\nColumns:", list(result.data.keys()) if hasattr(result, 'data') else result.columns.tolist())
    
#     # Display sample data
#     print(f"\n{'Index':<5} {'Close':<8} {'SUPERT':<12} {'Direction':<10}")
#     print("-" * 40)
    
#     try:
#         # Try pandas DataFrame access
#         supert_col = [col for col in result.columns if col.startswith('SUPERT') and not col.endswith('d') and not col.endswith('l') and not col.endswith('s')][0]
#         dir_col = [col for col in result.columns if col.endswith('d')][0]
        
#         for i in range(len(close_prices)):
#             close_val = close_prices[i]
#             supert_val = result[supert_col].iloc[i]
#             dir_val = result[dir_col].iloc[i]
#             direction_str = "LONG" if dir_val == 1 else "SHORT"
#             print(f"{i:<5} {close_val:<8} {supert_val:<12.2f} {direction_str:<10}")
            
#     except (AttributeError, ImportError):
#         # Fallback for simple DataFrame
#         supert_col = [col for col in result.data.keys() if col.startswith('SUPERT') and not col.endswith('d') and not col.endswith('l') and not col.endswith('s')][0]
#         dir_col = [col for col in result.data.keys() if col.endswith('d')][0]
        
#         for i in range(len(close_prices)):
#             close_val = close_prices[i]
#             supert_val = result.data[supert_col][i]
#             dir_val = result.data[dir_col][i]
#             direction_str = "LONG" if dir_val == 1 else "SHORT"
#             print(f"{i:<5} {close_val:<8} {supert_val:<12.2f} {direction_str:<10}")

import pendulum as dt
import pandas as pd
import pandas_ta as ta
# ta.supertrend()
import time
import logging


from datetime import datetime,timedelta
from zoneinfo import ZoneInfo

from alpaca.data.timeframe import TimeFrame, TimeFrameUnit

from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.requests import StopOrderRequest,StopLimitOrderRequest

from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetOrdersRequest
from alpaca.trading.enums import OrderSide, QueryOrderStatus,TimeInForce

from alpaca.data.historical import CryptoHistoricalDataClient
crypto_historical_data_client = CryptoHistoricalDataClient()
from zoneinfo import ZoneInfo
from alpaca.data.requests import CryptoBarsRequest

api_key='PKCGQ99MC5FQA1P8ZSRE'
secret_key='rkWLI1F2poiTbuERdzozfOLgVV6mrFKTH27Ugvb1'
list_of_tickers=["AAVE/USD","ETH/USD"]


#timframe is 1 min
time_frame=1
time_frame_unit=TimeFrameUnit.Minute
days=20
start_hour,start_min=13,31
end_hour,end_min=15,35
time_zone='America/New_York'
strategy_name='crypto_supertrend_ema_strategy'
stop_perc=1


#logging to file
logging.basicConfig(level=logging.INFO, filename=f'{strategy_name}_{dt.now(time_zone).date()}.log',filemode='a',format="%(asctime)s - %(message)s")


trading_client = TradingClient(api_key, secret_key, paper=True)



# def supertrend(high, low, close, length=None, multiplier=None, offset=None, **kwargs):
#     # Validate and set default parameters
#     length = int(length) if length and length > 0 else 7
#     multiplier = float(multiplier) if multiplier and multiplier > 0 else 3.0
#     offset = int(offset) if offset else 0
    
#     m = len(close)
#     # Validate series length
#     if m < length or len(high) != m or len(low) != m:
#         return None
    
#     # Initialize arrays
#     dir_ = [1] * m
#     trend = [None] * m
#     long = [None] * m
#     short = [None] * m
    
#     # Calculate HL2 and ATR
#     hl2_ = hl2(high, low)
#     atr_values = atr(high, low, close, length)
    
#     # Compute upper and lower bands
#     upperband = [None] * m
#     lowerband = [None] * m
#     for i in range(m):
#         if atr_values[i] is not None:
#             upperband[i] = hl2_[i] + multiplier * atr_values[i]
#             lowerband[i] = hl2_[i] - multiplier * atr_values[i]
    
#     # Process Supertrend logic starting from the 'length' index
#     for i in range(length, m):
#         if close[i] > upperband[i-1]:
#             dir_[i] = 1
#         elif close[i] < lowerband[i-1]:
#             dir_[i] = -1
#         else:
#             dir_[i] = dir_[i-1]
#             if dir_[i] == 1 and lowerband[i] < lowerband[i-1]:
#                 lowerband[i] = lowerband[i-1]
#             elif dir_[i] == -1 and upperband[i] > upperband[i-1]:
#                 upperband[i] = upperband[i-1]
        
#         if dir_[i] == 1:
#             trend[i] = lowerband[i]
#             long[i] = lowerband[i]
#         else:
#             trend[i] = upperband[i]
#             short[i] = upperband[i]
    
#     # Apply offset if needed
#     if offset != 0:
#         trend = shift_list(trend, offset)
#         dir_ = shift_list(dir_, offset)
#         long = shift_list(long, offset)
#         short = shift_list(short, offset)
    
#     # Handle fillna parameters
#     fill_value = kwargs.get('fillna', None)
#     fill_method = kwargs.get('fill_method', None)
    
#     trend = fillna(trend, fill_value, fill_method)
#     dir_ = fillna(dir_, fill_value, fill_method)
#     long = fillna(long, fill_value, fill_method)
#     short = fillna(short, fill_value, fill_method)
    
#     # Prepare result dictionary
#     _props = f"_{length}_{multiplier}"
#     return {
#         f"SUPERT{_props}": trend,
#         f"SUPERTd{_props}": dir_,
#         f"SUPERTl{_props}": long,
#         f"SUPERTs{_props}": short
#     }




def get_historical_crypto_data(ticker,duration,time_frame_unit):
    """extracts historical data and outputs in the form of dataframe"""
    now = datetime.now(ZoneInfo("America/New_York"))
    req = CryptoBarsRequest(
        symbol_or_symbols = ticker,
        timeframe=TimeFrame(amount = 1, unit = time_frame_unit), # specify timeframe
        start = now - timedelta(days = duration),                          # specify start datetime, default=the beginning of the current day.
        # end_date=None,                                        # specify end datetime, default=now
        # limit = 2,                                               # specify limit
    )
    history_df1=crypto_historical_data_client.get_crypto_bars(req).df
    sdata=history_df1.reset_index().drop('symbol',axis=1)
    sdata['timestamp']=sdata['timestamp'].dt.tz_convert('America/New_York')
    sdata=sdata.set_index('timestamp')
    sdata['ema']=ema(sdata['close'],length=10)
    d=supertrend(sdata.high,sdata.low,sdata.close,length=10)
    sdata['super']=supertrend(sdata.high,sdata.low,sdata.close,length=10)['SUPERTd_10_3.0']
    # sdata['atr']=ta.atr(sdata.high, sdata.low, sdata.close, length=14)

    return sdata

df=get_historical_crypto_data('BTC/USD',30,TimeFrameUnit.Hour)
print(df)

# def get_open_position():

#     pos=trading_client.get_all_positions()
#     new_pos=[]
#     for elem in pos:
#         new_pos.append(dict(elem))

#     pos_df=pd.DataFrame(new_pos)
#     print(pos_df)
#     #filter pos that are in list_of_tickers
#     l=[i.replace("/","") for i in list_of_tickers]
#     pos_df=pos_df[pos_df['symbol'].str.replace('/','').isin(l)]
#     return pos_df

# def get_open_orders():
#     # params to filter orders by
#     request_params = GetOrdersRequest(
#                         status=QueryOrderStatus.OPEN
#                     )

#     # orders that satisfy params
#     orders = trading_client.get_orders(filter=request_params)
#     new_order=[]
#     for elem in orders:
#         new_order.append(dict(elem))

#     order_df=pd.DataFrame(new_order)
#     #filter orders that are in list_of_tickers
#     if not order_df.empty:
#         order_df=order_df[order_df['symbol'].isin(list_of_tickers)]
#     return order_df




# def close_this_crypto_position(ticker_name):
#     try:
#         position = trading_client.get_open_position(ticker_name)
#         print(position)
#         logging.info(f'Closing position for {ticker_name}')
#         c=trading_client.close_position(ticker_name)
#         print(c)
#         print('position closed')
#     except:
#         print('position does not exist')

# def close_this_order_for_crypto(ticker_name):
#     order_df=get_open_orders()
#     if not order_df.empty:
#         order_df=order_df[order_df['symbol']==ticker_name]
#         print(order_df)
#         if not order_df.empty:
#             for id in order_df['id'].to_list():
#                 try:
#                     logging.info(f'Closing order for {ticker_name}')
#                     response = trading_client.cancel_order_by_id(id)
#                     print(response)
#                 except:
#                     print('order does not exist',ticker_name)
                

# def check_market_order_placed(ticker):
#     order_df=get_open_orders()
#     if not order_df.empty:
#         order_df=order_df[order_df['order_type']=='market']
#         if not order_df.empty and (ticker in order_df['symbol'].to_list()):
#             return 0
#         else:
#             return 1
#     else:
#         return 1



# def trade_sell_stocks(symbol,stock_price,stop_price,quantity=1):
#     logging.info(f'Selling {quantity} of {symbol} at {stock_price}')
#     if check_market_order_placed(symbol):

#         market_order_data = MarketOrderRequest(
#                             symbol=symbol,
#                             qty=quantity,
#                             side=OrderSide.SELL,
#                             time_in_force=TimeInForce.GTC
#                             )

#         # Market order
#         market_order = trading_client.submit_order(
#                         order_data=market_order_data
#                     )
#         print(market_order)




# def trade_buy_stocks(symbol,stock_price,stop_price,quantity=1):
#     logging.info(f'Buying {quantity} of {symbol} at {stock_price}')

#     if check_market_order_placed(symbol):

#         market_order_data = MarketOrderRequest(
#                             symbol=symbol,
#                             qty=quantity,
#                             side=OrderSide.BUY,
#                             time_in_force=TimeInForce.GTC
#                             )

#         # Market order
#         market_order = trading_client.submit_order(
#                         order_data=market_order_data
#                     )
#         print(market_order)


# def place_stop_order_stock(symbol,stop_price,quantity,side):
#     logging.info(f'Placing stop order for {quantity} of {symbol} at {stop_price}')
#     print('placing stop order')
#     req = StopLimitOrderRequest(
#                     symbol = symbol,
#                     qty = quantity,
#                     side = side,
#                     time_in_force = TimeInForce.GTC,
#                     limit_price = round(stop_price,2),
#                     stop_price = round(stop_price,2)
#                     )

#     res = trading_client.submit_order(req)
#     res


#     # stop_order_data=StopOrderRequest(
#     #                     symbol=symbol,
#     #                     stop_price=int(stop_price),
#     #                     qty=quantity,
#     #                     side=side,
#     #                     time_in_force=TimeInForce.GTC
#     # )

#     # stop_market_order = trading_client.submit_order(
#     #                 order_data=stop_order_data
#     #             )
#     print(res)


# def check_and_place_stop_order(pos_df,order_df):

#         if not pos_df.empty:
#             print('inside check and place stop order')
#             l1=pos_df['symbol'].to_list()
#             print(l1)
#             print(list_of_tickers)
#             #common stock in l1 and list_of_tickers
#             l1=list(set(l1).intersection(set([l.replace('/','') for l in list_of_tickers])))
            
#             print(l1)
#             for ticker in list_of_tickers:
#                 #check if stop order exist
#                 try:
#                         t=trading_client.get_open_position(ticker.replace('/',''))  
#                         buy_price=float(t.avg_entry_price)
#                         quantity=abs(round(float(t.qty),2))
#                         s=t.side
#                         if s==OrderSide.BUY:
#                             s=OrderSide.SELL
#                             stop_price=buy_price-buy_price*(1-(stop_perc/100))
#                         else:
#                             s=OrderSide.BUY
#                             stop_price=buy_price+buy_price*(1-(stop_perc/100))
#                         if order_df.empty or (ticker not in order_df['symbol'].to_list()):
#                             place_stop_order_stock(ticker,stop_price,quantity,s)
#                         print('stop order already placed')
#                 except Exception as e:
#                     print(e)
#                     print('stop order cannot be placed')
#                     logging.info(f'Stop order cannot be placed for {ticker}')


# def strategy_condition(hist_df_hourly,hist_df_daily,ticker):
#     print('inside strategy conditional code ')
#     # print(hist_df)
#     print(ticker)
#     buy_condition=hist_df_hourly['super'].iloc[-1]>0 and hist_df_daily['ema'].iloc[-1]<hist_df_hourly['close'].iloc[-1]
#     # buy_condition=True
#     # sell_condition=hist_df_hourly['super'].iloc[-1]<0 and hist_df_daily['ema'].iloc[-1]>hist_df_hourly['close'].iloc[-1]
#     # sell_condition=True


#     hourly_closing_price=hist_df_hourly['close'].iloc[-1]
#     atr_value=hist_df_daily['atr'].iloc[-1]

#     if buy_condition:
#         print('buy condition satisfied')
#         trade_buy_stocks(ticker,hourly_closing_price,hourly_closing_price-atr_value)
#     # elif sell_condition:
#     #     print('sell condition satisfied')
#     #     trade_sell_stocks(ticker,hourly_closing_price,hourly_closing_price+atr_value)
#     else:
#         print('no condition satisfied')

# def main_strategy():
#     pos_df= get_open_position()
#     ord_df= get_open_orders()
#     print(pos_df)
#     print(ord_df)
#     ord_df.to_csv('orders.csv')

#     for ticker in list_of_tickers:
#         print(ticker)
#         #historical data with indicator data
#         hist_df=get_historical_crypto_data(ticker,days,time_frame_unit)
#         print(hist_df)
#         hist_df_hourly=get_historical_crypto_data(ticker,10,TimeFrameUnit.Hour)
#         hist_df_daily=get_historical_crypto_data(ticker,50,TimeFrameUnit.Day)
#         print(hist_df_hourly)
#         print(hist_df_daily)

#         #get current money
#         money=float(trading_client.get_account().cash)
#         print(money)
#         # money=500
#         closing_price=hist_df['close'].iloc[-1]
#         print(closing_price)
#         quantity=money/closing_price
#         print(quantity)


#         if quantity<1:
#             continue
        


#         elif (pos_df.empty )  or (len(pos_df)!=0 and ticker.replace('/','') not in pos_df['symbol'].to_list()):
#             print('we have some position but ticker is not in pos')
#             strategy_condition(hist_df_hourly,hist_df_daily,ticker)

#         elif len(pos_df)!=0 and ticker.replace('/','')  in pos_df['symbol'].to_list():
#             print('we have some pos and ticker is in pos')
#             curr_quant=float(pos_df[pos_df['symbol']==ticker.replace('/','')]['qty'].iloc[-1])
#             print(curr_quant)
#             if curr_quant==0:
#                 print('my quantity is 0')
#                 strategy_condition(hist_df_hourly,hist_df_daily,ticker)
#             elif curr_quant>0:
#                 print('we are already long')
#                 sell_condition=hist_df_hourly['super'].iloc[-1]<0 and hist_df_daily['ema'].iloc[-1]>hist_df_hourly['close'].iloc[-1]
#                 if sell_condition:
#                     print('sell condition is satisfied ')
#                     logging.info(f'Sell condition satisfied for {ticker}')
#                     close_this_crypto_position(ticker)
#                 else:
#                     print('sell condition not satisfied')
        
#     time.sleep(1)
#     check_and_place_stop_order(pos_df,ord_df)

# main_strategy()

# current_time=dt.now(time_zone)
# print(current_time)
# start_time=dt.datetime(current_time.year,current_time.month,current_time.day,start_hour,start_min,tz=time_zone)
# end_time=dt.datetime(current_time.year,current_time.month,current_time.day,end_hour,end_min,tz=time_zone)
# print('start time:', start_time)
# print('end time:', end_time)


# #pre hour and post hour

# while dt.now(time_zone)<start_time :
#     print(dt.now(time_zone))
#     time.sleep(1)

# print('we have reached start time ')
# print('we are running our strategy now')


# while True:
#     if dt.now(time_zone)>end_time:
#         break
#     ct=dt.now(time_zone)
#     print(ct)
#     if ct.second in range(2,3) and ct.minute in range(0,60,time_frame):
#         # ct.second in range(2,4) and ct.minute==1
#         main_strategy()
#     time.sleep(1)




# print('we have reached end time')


# #close all orders
# for ticker in list_of_tickers:
#     close_this_order_for_crypto(ticker)
#     print('order closed')



# pos_df= get_open_position()
# l1=pos_df['symbol'].to_list()
# l1=list(set(l1).intersection(set([l.replace('/','') for l in list_of_tickers])))
# #close all positions
# for ticker in l1:
#     close_this_crypto_position(ticker)
#     print('position closed')


# print('strategy stopped')