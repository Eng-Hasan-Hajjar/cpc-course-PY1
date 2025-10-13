# lesson8
txt = "Hello, welcome to my world."
x = txt.endswith(".")
print(x)


txt = "Hello, welcome to my world."
x = txt.endswith("my world.", 5, 11)
print(x)


txt = "Hello, welcome to my world."
x = txt.find("welcome")
print(x)


txt = "Hello, welcome to my world."
x = txt.find("e")
print(x)


txt = "Hello, welcome to my world."
x = txt.find("e", 5, 10)
print(x)




txt = "Hello, welcome to my world."
print(txt.find("q"))
### print(txt.index("q"))



txt = "Hello, welcome to my world."
x = txt.index("welcome")
print(x)

txt = "hello world!"
x = txt.islower()
print(x)


a = "Hello world!"
b = "hello 123"
c = "mynameisPeter"
print(a.islower())
print(b.islower())
print(c.islower())

myTuple = ("John", "Peter", "Vicky")
x = "#".join(myTuple)
print(x)


myTuple = ["John", "Peter", "Vicky"]
x = " & ".join(myTuple)
print(x)



myDict = {"name": "John", "country": "Norway"}
mySeparator = "TEST"
x = mySeparator.join(myDict)
print(x)



txt = "        banana     "
x = txt.lstrip()
print("of all fruits", x, "is my favorite")


txt = ",,,,,ssaaww.....bananaasw"
x = txt.lstrip(",.as")
print(x)


txt = "I could eat bananas all day"
x = txt.partition("apples")
print(x)


txt = "I could eat bananas all day"
x = txt.partition("I")
print(x)



txt = "I could eat  I bananas  I all day"
x = txt.partition("I")
print(x)

txt = "I like bananas"
x = txt.replace("bananas", "apples")
print(x)

txt = "one one was a race horse, two two was one too."
x = txt.replace("one", "three")
print(x)

txt = "one one was a race horse, two two was one too."
x = txt.replace("one", "three", 2)
print(x)
txt = "Mi casa, su casa."
x = txt.rfind("casa")
print(x)



txt = "welcome to the jungle"
x = txt.split()
print(x)


txt = "hello, my name is Peter, I am 26 years old"
x = txt.split(", ")
print(x)

txt = "apple#banana#cherry#orange"
x = txt.split("#")
print(x)




txt = "Thank you for the music\nWelcome to the jungle"
x = txt.splitlines()
print(x)



txt = "Hello My Name Is PETER"
x = txt.swapcase()
print(x)



txt = "Welcome to my world"
x = txt.title()
print(x)