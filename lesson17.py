##lesson17
class Person:
    def __init__(self,name2,age2):
        self.name=name2
        self.age=age2
    def print_name(self):
        print(self.name ,"\n",self.age)

marcel=Person("maecel",19)
omar_madarati=Person("omar",20)
abd_elah=Person("abd",20)

marcel.print_name()
omar_madarati.print_name()
abd_elah.print_name()


print(marcel.name)
print(marcel.__str__())