class Person:
    def __init__(self,name,age,number,gender):
        self.name=name
        self.age=age
        self.number=number
        self.gender=gender


#lesson19

class Student(Person):
    def __init__(self,name,age,number,gender, num_course):
        Person.__init__(self,name,age,number,gender)
        self.num_course = num_course

    def print_object (self):
        print( f"Name: {self.name}, Age: {self.age}, Number: {self.number}, num_course: {self.num_course}")
    #تابع استدعاء الاسم فقط
    def print_name_of_object (self):
        print(f"Name: {self.name}")

class teacher(Person):
    def __init__(self,name,age,number, gender, num_course_learn, salary):
        super().__init__(name,age,number,gender)
        self.num_course_learn = num_course_learn
        self.salary= salary

    def print_object (self):
        print( f"Name: {self.name}, Age: {self.age}, Number: {self.number}, num_course_learn: {self.num_course_learn},salary: {self.salary}")

#تابع استدعاء الاسم فقط
    def print_name_of_object (self):
        print(f"Name: {self.name}")

class employee(Person):
    def __init__(self,name,age,number, gender, rule):
        Person.__init__(self,name,age,number,gender)

        self.rule = rule

    def print_object (self):
        print( f"Name: {self.name}, Age: {self.age}, Number: {self.number}, rule: {self.rule}")
    #تابع استدعاء الاسم فقط
    def print_name_of_object (self):
        print(f"Name: {self.name}")
    #استدعاء الدور
    def print_rule_of_object (self):
         print(f"Name: {self.rule}")




#main


student1 = Student("Alice", 20, "S123","male", 5)
teacher1 = teacher("Mr. Smith", 40, "T456","male", 3, 50000)
employee1 = employee("Bob", 30, "E789","male", "Manager")

student1.print_object()
teacher1.print_object()
employee1.print_object()

student1.print_name_of_object()
employee1.print_name_of_object()
employee1.print_rule_of_object()