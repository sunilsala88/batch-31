
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