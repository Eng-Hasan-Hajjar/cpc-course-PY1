#lesson18

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    def __str__(self):
        return f"{self.name}({self.age})"


p1 = Person("John", 36)
print(p1)




class Person:
 def __init__(mysillyobject, name, age):
        mysillyobject.name = name
        mysillyobject.age = age
 def myfunc(abc):
        print("Hello my name is " + abc.name)
p1 = Person("John", 36)
p1.myfunc()
p1.age = 40
del p1.age

del p1
class Person:
 pass





class Player:
    def __init__(self, name, health=100):
        self.name = name
        self.health = health
        self.inventory = []
        self.position = (0, 0)
    def move(self, x, y):
        self.position = (x, y)
        print(f"{self.name} moved to position {self.position}")
    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
           print(f"{self.name} has been eliminated!")
        else:
           print(f"{self.name} took {damage} damage, {self.health} health remaining")
    def pick_up_weapon(self, weapon):
        self.inventory.append(weapon)
        print(f"{self.name} picked up {weapon.name}")
    def  medicen(self,med):
        self.health+=med
        if self.health>=100:
            self.health=100

class Weapon:
    def __init__(self, name, damage):
        self.name = name
        self.damage = damage
    def __str__(self):
        return self.name



akm = Weapon("AKM", 49)
m416 = Weapon("M416", 43)
om=Weapon("om",150)





class Vehicle:
    def __init__(self, type, max_speed, health=1000):
        self.type = type
        self.max_speed = max_speed
        self.health = health
    def drive(self, destination):
        print(f"Driving {self.type} to {destination} at max speed of {self.max_speed} km/h")
    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
         print(f"The {self.type} has been destroyed!")
        else:
         print(f"The {self.type} took {damage} damage, {self.health} health remaining")

buggy = Vehicle("Buggy", 90)
buggy.drive("Pochinki")
buggy.take_damage(50)



class Map:
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.players = []
        self.vehicles = []
    def add_player(self, player):
        self.players.append(player)
        print(f"{player.name} joined the map {self.name}")
    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)
        print(f"{vehicle.type} added to the map {self.name}")



player1 = Player("Fouado")

erangel = Map("Erangel", "8x8 km")
erangel.add_player(player1)
erangel.add_vehicle(buggy)






















































































































































































