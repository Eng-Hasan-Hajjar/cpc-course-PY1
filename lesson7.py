#lesson7


student1="omar"
student2="AbdElah"
all_students=student1+" and " + student2
print(all_students)


#Python - Format - Strings
age = 36
#This will produce an error:
txt = "My name is John, I am " + str(age)
print(txt)




age = 36
txt = f"My name is John, I am {age}"
print(txt)

price = 59
txt = f"The price is {price} dollars"
print(txt)

price = 59
txt = f"The price is {price:.3f} dollars"
print(txt)


txt = f"The price is {20 * 59} dollars"
print(txt)


txt = f"The price is 20 * 59 dollars"
print(txt)


#Python - Escape Characters
txt = "We are the so-called \"Vikings\" from the north."
print(txt)

#txt = "Hello \n  World!"
#print(txt) 
txt = "Hello\tWorld!"
print(txt) 

#Python - String Methods
txt = "hello, and welcome to my world."
x = txt.capitalize()
print (x)
txt = "hello, and welcome to my world. "
x = txt.title()
print (x)
txt = "Hello, And Welcome To My World!"
x = txt.casefold()
print(x)


txt = "Hello, And Welcome To My World!"
x = txt.lower()
print(x)


txt = "banana"
x = txt.center(20)
print(x)




txt = "banana"
x = txt.center(20,"*")
print(x)


txt = "I love apples, apple are my favorite fruit"
x = txt.count("apple")
print(x)
