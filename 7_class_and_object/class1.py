#class
#class is blueprint of object

#object
#object is the instance of a class

#attribute/char
#any variable that you create inside a class is called a attribute

#class attribute
#variable which is common for all object 

#instance attribute
#variable which is unique for each object 

#method
#any function that you create inside a class is called method

#contructor
#function which is executed when you create a object

class Car:
    wheel=4
    window='glass'

    #constructor
    def __init__(self,brand,color,car_num):
        self.brand=brand
        self.color=color
        self.car_num=car_num
        
    
    def introduce(self):
        return f"this car brand is {self.brand} and color is {self.color} and we have {self.wheel} wheels"
def introduce():
        return f"this car brand is  and color is and we have wheels"



c1=Car(brand='bmw',color='blue',car_num=123)
c2=Car(brand='audi',color='black',car_num=567)
print(c1.window)
print(c2.car_num)
print(c1.introduce())
print(c2.introduce())


class Student:
    school_name='dji'
    dress_code='black_white'

    def __init__(self,name,email,roll_no,phone):
        self.name=name
        self.email=email
        self.rool_num=roll_no
        self.phone_num=phone
    
    def introduce(self):
        return f"my name is {self.name} and my email is {self.email}"

s1=Student('raj','raj@gmail.com',33,993029)
s2=Student('don','don@gmail.com',66,884738)
print(s1.rool_num)
print(s2.rool_num)
print(s1.phone_num)
print(s2.phone_num)
print(s1.introduce())


