#lesson4
#functions


x=12

def type_abdelaah():
    print("this is first function with cpc python course")
    print(x)



print("out of function:  ",x)


type_abdelaah()






#ex2

y=12
def type_abdelaah():
    print("this is first function with cpc python course")
    y=10
    print(y)

print("out of function:  ",y)
type_abdelaah()
print("out of function after:  ",y)






#ex3

z=12

def type_abdelaah():
    print("this is first function with cpc python course")
    global z
    z=10
    print(z)
print("out of function:  ",z)
type_abdelaah()
print("out of function after:  ",z)



#data types
c=3+2j
print(type(c))


x=-2j
print(type(x))

#list
laptops=["hp","toshipa","del","Mac"]
print(type(laptops))
#tuple
laptops=("hp","toshipa","del","Mac")
print(type(laptops))


#set
laptops={"hp","toshipa","del","Mac"}
print(type(laptops))

#dictionary
laptop={"brand":"hp","year":2025,"gen":13}
print(type(laptop))


#rang
s=range(6)
print(type(s),s)


