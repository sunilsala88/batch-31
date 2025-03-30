
prices=[22,33,44,55,93,23]

#type 1 loop
#sum of all the element
total=0
for num in prices:
    total=total+num

print('total is',total)

max1=prices[0]

for num in prices:
    if num>max1:
        max1=num
print('maximum value is',max1)

#min value in a list

min1=prices[0]

for num in prices:
    if num<min1:
        min1=num
print('maximum value is',min1)