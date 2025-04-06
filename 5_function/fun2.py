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