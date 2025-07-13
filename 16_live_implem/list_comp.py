

list1=[1,2,3,4]
# list2=[]
# for i in list1:
#     list2.append(i**2)
# print(list2)

list2= [i**2 for i in list1]
print(list2)






import pendulum as dt
import pandas as pd
import pandas_ta as ta
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


trading_client = TradingClient(api_key, secret_key, paper=True)


#timframe is 1 min
time_frame=1
time_frame_unit=TimeFrameUnit.Minute
days=20
start_hour,start_min=13,31
end_hour,end_min=15,35
time_zone='America/New_York'
strategy_name='crypto_supertrend_ema_strategy'
stop_perc=1


def get_open_position():

    pos=trading_client.get_all_positions()
    new_pos=[]
    for elem in pos:
        new_pos.append(dict(elem))

    pos_df=pd.DataFrame(new_pos)
    print(pos_df)
    #filter pos that are in list_of_tickers
    # l=[i.replace("/","") for i in list_of_tickers]
    # pos_df=pos_df[pos_df['symbol'].str.replace('/','').isin(l)]
    return pos_df


df=get_open_position()
print(df)

# df.to_csv('pos.csv')

# l1=[]
# for i in df['exchange']:
#     print(i)
#     print(type(i))

print(df.columns)
print(df.info())
df['qty']=df['qty'].astype('float')
a=df[df['qty']>0]['symbol'].to_list()
print(a)

list_of_tickers=["DOGE/USD","ETH/USD"]

b1=[]
for i in list_of_tickers:
    b1.append(i.replace('/',''))


l1=df['symbol'].to_list()
print(l1)
print(list_of_tickers)
l2=list(set(l1).intersection(set([l.replace('/','') for l in list_of_tickers])))
print(l2)