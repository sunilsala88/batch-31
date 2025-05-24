

from finvizfinance.quote import finvizfinance

symbols=['tsla','amzn','goog']
data={}
d='P/B'
# stock = finvizfinance('tsla')

stock = finvizfinance('tsla').ticker_full_info()
# print(stock)


# for name in symbols:
#     stock = finvizfinance(name).ticker_full_info()
#     print(stock)
#     v=stock.get('fundament').get(d)
#     data.update({name:v})
# print(data)


from finvizfinance.screener.overview import Overview

foverview = Overview()
filters_dict = {'Index':'NASDAQ 100','Sector':'Technology'}
foverview.set_filter(filters_dict=filters_dict)
df = foverview.screener_view()
print(df)
df.to_csv('data.csv')