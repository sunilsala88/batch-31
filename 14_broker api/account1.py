from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame

# no keys required for crypto data
client = CryptoHistoricalDataClient()

request_params = CryptoBarsRequest(
                        symbol_or_symbols=["BTC/USD", "ETH/USD"],
                        timeframe=TimeFrame.Day,
                        start="2022-07-01"
                 )

bars = client.get_crypto_bars(request_params).df
print(bars)

api_key='PKCGQ99MC5FQA1P8ZSRE'
secret_key='rkWLI1F2poiTbuERdzozfOLgVV6mrFKTH27Ugvb1'


from alpaca.trading.client import TradingClient

trading_client = TradingClient(api_key, secret_key, paper=True)

account = trading_client.get_account()
print(account)
print(account.cash)
print(account.portfolio_value)
print(account.buying_power)

print(trading_client.get_all_positions())

# id=UUID('28959f70-ced0-4150-a908-c1d2ef1a475a') 
# account_number='PA32II6CTZQA' 
# status=<AccountStatus.ACTIVE: 'ACTIVE'> 
# crypto_status=<AccountStatus.ACTIVE: 'ACTIVE'> currency='USD' 
# buying_power='597780.84' 
# regt_buying_power='227178.91' 
# daytrading_buying_power='597780.84' 
# non_marginable_buying_power='111589.45' 
# cash='25115.81' 
# accrued_fees='0' 
# pending_transfer_out=None 
# pending_transfer_in=None 
# portfolio_value='1034073.51' 
# pattern_day_trader=True 
# trading_blocked=False 
# transfers_blocked=False 
# account_blocked=False 
# created_at=datetime.datetime(2024, 8, 24, 9, 13, 29, 133143, tzinfo=TzInfo(UTC)) 
# trade_suspended_by_user=False 
# multiplier='4' 
# shorting_enabled=True 
# equity='1034073.51' 
# last_equity='1029364.9163546246' 
# long_market_value='1009540.57' 
# short_market_value='-582.87' 
# initial_margin='89639.39' 
# maintenance_margin='53783.63' 
# last_maintenance_margin='53783.63' 
# sma='203429.63' 
# daytrade_count=0 
# options_buying_power='111589.45' 
# options_approved_level=3 
# options_trading_level=3