
#https://colab.research.google.com/drive/1rspCrN8NEsEjeYmmN1pG0gDmvP8WswE3?usp=sharing

#pip install yfinance
import yfinance as yf
# data=yf.download('TSLA',multi_level_index=False)
# print(data)
# print(data.columns)
# l1=[]
# for i in data.columns:
#     l1.append(i[0])
# data.columns=l1
# print(data)
# d=yf.download(['TSLA','AMZN'],multi_level_index=False)
# print(d)


# data=yf.download('TSLA',multi_level_index=False,period='5mo')
# print(data)

# data=yf.download('TSLA',multi_level_index=False,start='2024-01-01',end='2024-12-30')
# print(data)

# import datetime as dt
# s=dt.datetime(2023,1,1)
# e=dt.datetime(2023,12,30)
# data=yf.download('TSLA',multi_level_index=False,start=s,end=e)
# print(data)

# data=yf.download('BTC-USD',multi_level_index=False,start='2024-01-01',end='2024-12-30',interval='30m')
# print(data)


data=yf.download('TSLA',multi_level_index=False,period='7d',interval='1m')
print(data)
data=yf.download('RELIANCE.NS',multi_level_index=False,period='7d',interval='1m')
print(data)
data=yf.download('RELIANCE.NS',multi_level_index=False,period='7d',interval='1m',ignore_tz=True)
print(data)