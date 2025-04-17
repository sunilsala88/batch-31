
f=open('error.txt','a')

try:
    num1=int(input('enter num 1'))
    num2=int(input('enter num 2'))

    ans=num1/num2
    print(ans)
except Exception as e:
    print('something happened')
    print(e)
    f.write(str(e))
    f.write('\n')
f.close()

print('important line')