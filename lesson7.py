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