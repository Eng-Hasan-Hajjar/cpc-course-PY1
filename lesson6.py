##lesson6
txt = "The best things in life are free!"
if "free" in txt:
  print("Yes, 'free' is present.")




txt = "The best things in life are free!"
if "fuck" not in txt:
  print("not, 'fuck' is not present.")


txt = "The best things in life are free!"
print("expensive" not in txt)


txt = "The best things in life are free!"
if "expensive" not in txt:
  print("No, 'expensive' is NOT present.")


b = "Hello, World!"
print(b[2:5])  


b = "Hello, World!"
print(b[:5])


b = "Hello, World!"
print(b[2:])

b = "Hello, World!"
print(b[-5:-2])


#Python - Modify Strings
a = "Hello, World!"
print(a.upper())


a = "Hello, World!"
print(a.lower())



a = " Hello,      World! "
print(a.strip()) # returns "Hello, World!"



a = "Hello, World!"
print(a.replace("H", "J"))


a = "Hello, Horld!"
print(a.replace("H", "J"))

a = "Hello, World!"
print(a.split(",")) # returns ['Hello', ' World!']