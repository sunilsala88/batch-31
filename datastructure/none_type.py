
#flasy value
# 0, None, False, [], {}, set(), '', ()

#truthy value
#everything else
print(10<20)
stocks={
    'AAPL': [150,160,170],
    'MSFT': [250,260,270],
    'GOOGL': [2800,2900,3000]
}
v=stocks.get('GOOGL')
print(v)
if v:
    print(v)
else:
    print('it does not exist')



foreign_exchange = {
    "base_currency": "USD",
    "exchange_rates": {
        "EUR": {
            "current_rate": 0.85,
            "historical_rates": [
                {"date": "2024-01-10", "rate": 0.84},
                {"date": "2024-01-09", "rate": 0.85}
            ]
        },
        "JPY": {
            "current_rate": 110.00,
            "historical_rates": [
                {"date": "2024-01-10", "rate": 109.50},
                {"date": "2024-01-09", "rate": 110.20}
            ]
        }
    }
}
