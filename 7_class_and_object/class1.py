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
    
    def __str__(self):
         return self.name
    
    def introduce(self):
        return f"my name is {self.name} and my email is {self.email}"

s1=Student('raj','raj@gmail.com',33,993029)
s2=Student('don','don@gmail.com',66,884738)
print(s1.rool_num)
print(s2.rool_num)
print(s1.phone_num)
print(s2.phone_num)
print(s1.introduce())


class Book:
     
    def __init__(self,title, author, price, quantity):
          self.title=title
          self.author=author
          self.price=price
          self.quantity=quantity
    def __str__(self):
         return self.title
         
    
    def get_price(self):
        return self.price

    def set_price(self,new_price):
        self.price=new_price
    def get_quantity(self):
         return self.quantity
    
    def set_quantity(self, new_quantity): 
         self.quantity=new_quantity
    def sell(self, number_sold):
         self.quantity=self.quantity-number_sold
    def restock(self, number_added): 
         self.quantity=self.quantity+number_added

# Create a new book instance
my_book = Book(title="1984", author="George Orwell", price=29.99, quantity=100)

# Get and set price
print(my_book.get_price())  # Output: 29.99
my_book.set_price(24.99)
print(my_book.price)
print(my_book)
print(s2)

#area pi*(r**2)
#cir 2*pi*r

class Circle:
    pi=3.14

    def __init__ (self,radius):
        self.radius=radius

    def area(self):
        return self.pi*(self.radius**2)

    def circumference(self):
        return self.pi*2*self.radius

c1=Circle(5)
print(c1.area())
print(Circle.area(c1))


c2=Circle(10)
print(c2.area())
print(Circle.area(c2))
print(c2.pi)
c2.pi=66
print(c2.pi)
print(c1.pi)



class Broker:
    stock_prices={'goog':400,'amzn':900,'tsla':780}
     
    def __init__(self,name,acc_no,money):
          self.name=name
          self.acc_no=acc_no
          self.wallet=money
          self.portfolio={}
    
    def get_portfolio(self):
        if self.portfolio!={}:
             for i,j in self.portfolio.items():
                  print(i,j)
        else:
             print('empty')
    def buy(self,stock_name):
         pass
    
    def sell(self,stock_name):
         pass
         