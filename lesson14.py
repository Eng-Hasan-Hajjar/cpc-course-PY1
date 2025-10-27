#
# lesson14

x = {"apple", "banana", "cherry"}
y = {"google", "microsoft", "apple"}
z = x.intersection(y)
print(z)






set1 = {"apple", "banana", "cherry"}
set2 = {"google", "microsoft", "apple"}
set3 = set1 & set2
print(set3)


x = {"apple", "banana", "cherry"}
y = {"google", "microsoft", "apple"}
x.intersection_update(y)
print(z)



set1 = {"apple", "banana", "cherry"}
set2 = {"google", "microsoft", "apple"}
set3 = set1 - set2
print(set3)




x = {"apple", "banana", "cherry"}
y = {"google", "microsoft", "apple"}
x.symmetric_difference_update(y)
print(x)

set1 = {"apple", "banana", "cherry"}
set2 = {"google", "microsoft", "apple"}
set3 = set1 ^ set2
print(set3)




print("\n")

thisdict = {
 "brand": "Ford",
 "model": "Mustang",
 "year": 1964
}
print(thisdict)



thisdict = {
 "brand": "Ford",
 "model": "Mustang",
 "year": 1964
}
print(thisdict["brand"])




thisdict = {
 "brand": "Ford",
 "model": "Mustang",
 "year": 1964,
 "year": 2020
}
print(thisdict)

print(len(thisdict))


thisdict = {
 "brand": "Ford",
 "electric": False,
 "year": 1964,
 "colors": ["red", "white", "blue"]
}

thisdict = dict(name = "John", age = 36, country = "Norway")
print(thisdict)

thisdict = {
 "brand": "Ford",
 "model": "Mustang",
 "year": 1964
}
x = thisdict["model"]

print(x)
x = thisdict.get("model")
x = thisdict.keys()
car = {
 "brand": "Ford",
 "model": "Mustang",
 "year": 1964
}
x = car.keys()
print(x) #before the change
car["color"] = "white"
print(x) #after the change


x = thisdict.values()


car = {
 "brand": "Ford",
 "model": "Mustang",
 "year": 1964
}
x = car.values()
print(x) #before the change
car["year"] = 2020
print(x) #after the change




car = {
 "brand": "Ford",
 "model": "Mustang",
 "year": 1964
}
x = car.values()
print(x) #before the change
car["color"] = "red"
print(x) #after the change

car = {
 "brand": "Ford",
 "model": "Mustang",
 "year": 1964
}
x = car.items()
print(x) #before the change
car["year"] = 2020
print(x) #after the change





thisdict = {
 "brand": "Ford",
 "model": "Mustang",
 "year": 1964
}
if "model" in thisdict:
 print("Yes, 'model' is one of the keys in the thisdict dictionary")


thisdict = { "brand": "Ford", "model": "Mustang", "year": 1964}
thisdict["year"] = 2018


thisdict = { "brand": "Ford", "model": "Mustang", "year": 1964}
thisdict.update({"year": 2020})



thisdict = { "brand": "Ford","model": "Mustang","year": 1964}
thisdict.pop("model")
print(thisdict)


thisdict = { "brand": "Ford", "model": "Mustang", "year": 1964}
thisdict.popitem()
print(thisdict)


thisdict = { "brand": "Ford", "model": "Mustang", "year": 1964}
thisdict.clear()
print(thisdict)

thisdict = { "brand": "Ford", "model": "Mustang", "year": 1964}

for x, y in thisdict.items():
 print(x, y)


thisdict = { "brand": "Ford", "model": "Mustang", "year": 1964}
mydict = thisdict.copy()
print(mydict)











































































































































































