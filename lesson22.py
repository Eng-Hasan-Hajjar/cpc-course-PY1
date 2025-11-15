##lesson22
import os


if os.path.exists("demofile.txt"):
    os.remove("demofile.txt")
else:
    print("The file does not exist")

print(dir(os))


if os.path.exists("myfolder"):
    os.rmdir("myfolder")
else:
    print("The file does not exist")

print(dir(os))

try:
 print(x)
except:
 print("An exception occurred")

try:
 print(x)
except NameError:
 print("Variable x is not defined")
except:
 print("Something else went wrong")

try:
 print("Hello")
except:
 print("Something went wrong")
else:
 print("Nothing went wrong")




try:
 print(x)
except:
 print("Something went wrong")
finally:
 print("The 'try except' is finished")




try:
    f = open("demofile.txt")
    try:
        f.write("Lorum Ipsum")
    except:
        print("Something went wrong when writing to the file")
    finally:
        f.close()
except:
    print("Something went wrong when opening the file")



"""
x = -1
if x < 0:
 raise Exception("Sorry, no numbers below zero")


"""



x = 5
if not type(x) is int:
 raise TypeError("Only integers are allowed")

