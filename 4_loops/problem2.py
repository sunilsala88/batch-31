# stock_prices={'amzn': 555, 'tsla': 333, 'ongc': 667, 'reliance': 345, 'goog': 678}

# for i,j in stock_prices.items():
#     print(i,":",j)

# portfolio=[]

# while True:
#     stock_name=input('enter the stock name (press q to quit)')
#     print(stock_name)

#     if stock_name.upper()=='Q':
#         break

#     if stock_name=='ongc':
#         print('we cannot trade this stock')
#         continue

#     found=stock_prices.get(stock_name)
#     if found:
#         portfolio.append(stock_name)
#     else:
#         print('stock does not exist')

# print(portfolio)


# money=1000
# initial_money=money
# annual_ret=5
# years=0

# while True:
#     if money>2*initial_money:
#         break
#     money=money+(money*(annual_ret/100))
#     years=years+1

# print(years)

# list1=[44,55,66,7,5]

# new_list=[]
# index1=-1

# while True:

#     print(index1)
#     new_list.append(list1[index1])

#     if index1==len(list1)*(-1):
#         break
#     index1=index1-1
# print(new_list)

# string1='hello'

# new_string=""
# index1=-1

# while True:

#     print(index1)
#     new_string=new_string+string1[index1]

#     if index1==len(list1)*(-1):
#         break
#     index1=index1-1
# print(new_string)


# loan_amount=5000
# monthly_payment=200
# annual_rate=0.07

# months=0
# # amount=loan_amount
# while True:

#     if months%12==0:
#         loan_amount=loan_amount+(loan_amount*annual_rate)
#     loan_amount=loan_amount-monthly_payment

#     if loan_amount<0:
#         break
#     months=months+1

# print(months)



string1='racecr'

new_string=""
index1=-1
while True:

    print(index1)
    new_string=new_string+string1[index1]

    if index1==len(string1)*(-1):
        break
    index1=index1-1
print(new_string)
if string1==new_string:
    print('its a palindrome')
else:
    print('its not a palindrome')

list1=[3, 1, 4, 1, 5, 9]

list1.sort()
print(list1[-2])
