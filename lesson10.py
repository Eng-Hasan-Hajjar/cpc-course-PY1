#lesson10
customers=["elena","selena","helena"]
print(len(customers))

customers_euro=list(("alex","lucas","anglr","lux"))
print(type(customers_euro))

ages=[22,26,27]
isgood=[True,True,True]
print(customers[1])
print(customers[-1])

if("selena" in customers):
    print("selena exist")
else :
    print("selena is not fount")    


customers[0]="delena"
print(customers)
customers=["elena","selena","helena","morgana","inura"]
customers[3:]=["noura","mix"]
print(customers)

customers.insert(2,"kelena")
print(customers)
customers.append("daina")
print(customers)

customers_euro=list(("alex","lucas","anglr","lux"))

customers.extend(customers_euro)
print(customers)

if "Hasan" in customers:
    customers.remove("Hasan")
    print(customers)


customers.pop(1)
print(customers)


customers.pop(-1)
print(customers)


#del customers[0]
#del customers
#print(customers)
#customers.clear()
#print(customers)

for x in customers:
    print(x)

for i in range(len(customers)):
    print(customers[i])


i=0
while(i<len(customers)):
    print(customers[i]) 
    i+=1   

[print(x) for x in customers]


fruits = ["apple", "banana", "cherry", "kiwi", "mango"]
newlist = []
for x in fruits:
 if "a" in x:
  newlist.append(x)
print(newlist)




fruits = ["apple", "banana", "cherry", "kiwi", "mango"]
newlist = [x for x in fruits if "a" in x]
print(newlist)


thislist = ["orange", "mango", "kiwi", "pineapple", "banana"]
thislist.sort()
print(thislist)


thislist = ["orange", "mango", "kiwi", "pineapple", "banana"]
thislist.sort(reverse = True)
print(thislist)
