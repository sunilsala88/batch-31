
# name='jay'
# age=30
# sent='my name is '+name +' and my age is '+str(age)
# sent1=f"my name is {name} and my age is {age}"
# print(sent)
# print(sent1)

# # Function with parameters
# def add(num1: int, num2: int) -> int:
#     """Add two numbers"""
#     return num1 + num2

# # Calling the function
# result = add(num2=5,num1=10)
# print(f"The sum is: {result}")

# #args kwargs
# def myFun(*args):
#     print(args)
#     for arg in args:
#         print(arg)

# myFun("Hello", "World", "Python",1,2,3)

# def my_function(**kid):
#   print(kid)
#   print("His last name is " + kid["lname"])

# my_function(fname = "Tobias", lname = "Refsnes")


# #lambda function

# def square(num1):
#     return num1**2

# square = lambda x: x **2
# print(square(5))

def abc(num1):
    global a
    a=20
    print(num1)

a=11
print('hello')
abc(1)
print(a)
