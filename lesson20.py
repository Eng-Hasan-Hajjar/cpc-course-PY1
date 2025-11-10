#lesson 20
x = "Hello World!"
print(len(x))

mytuple = ("apple", "banana", "cherry")
print(len(mytuple))

thisdict = {
 "brand": "Ford",
 "model": "Mustang",
 "year": 1964
}
print(len(thisdict))

class Vehicle:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model 
    def move(self):
        print("Move!")

class Car(Vehicle):
  pass

class Boat(Vehicle):

    def move(self):
        print("Sail!")
class Plane(Vehicle):
    def move(self):
        print("Fly!")




car1 = Car("Ford", "Mustang") #Create a Car class
boat1 = Boat("Ibiza", "Touring 20") #Create a Boat class
plane1 = Plane("Boeing", "747") #Create a Plane class
for x in (car1, boat1, plane1):
    print(x.brand)
    print(x.model)
    x.move()


import json
# some JSON:
x = '{ "name":"John", "age":30, "city":"New York"}'
# parse x:
y = json.loads(x)
# the result is a Python dictionary:
print(y["age"])




import json
# a Python object (dict):
x = {
 "name": "John",
 "age": 30,
 "city": "New York"
}
# convert into JSON:
y = json.dumps(x)
# the result is a JSON string:
print(y)




print(json.dumps({"name": "John", "age": 30}))
print(json.dumps(["apple", "bananas"]))
print(json.dumps(("apple", "bananas")))
print(json.dumps("hello"))
print(json.dumps(42))
print(json.dumps(31.76))
print(json.dumps(True))
print(json.dumps(False))
print(json.dumps(None))





x = {
 "name": "John",
 "age": 30,
 "married": True,
 "divorced": False,
 "children": ("Ann","Billy"),
 "pets": None,
 "cars": [
 {"model": "BMW 230", "mpg": 27.5},
 {"model": "Ford Edge", "mpg": 24.1}
]
}
print(json.dumps(x, indent=4)
)

f = open("demofile.txt")
print(f.read())



