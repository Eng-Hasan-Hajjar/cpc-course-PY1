##lesson5
##Python Numbers

e=3
uu=3.2
j5=1+1j
print(e,uu,j5)


#integer
i=1234568987
print(i,type(i))




i=-1234568987
print(i,type(i))


##float
i=-1234568987.23
print(i,type(i))

i=-1234568987.23
print(i,type(i))


i=1587.0
print(i,type(i))

i=15e5
print(i,type(i))
i=15E5
print(i,type(i))
i=-15E5
print(i,type(i))
i=15E100
print(i,type(i))


##random
import random
print(dir(random))
print(random.randrange(0,5))

##casting
i=float(12)
print(i,type(i))
i=int(12.2)
print(i,type(i))
i=complex(12.2)
print(i,type(i))

i=float("12")
print(i,type(i))
i=int("12")
print(i,type(i))

i=str(12)
print(i,type(i))
i=str(12.5)
print(i,type(i))

#strings
#السلاسل
print("Omar")
print('omar')

print("It's alright")
print("He is called 'Johnny'")

print('He is called "Johnny"')

r="fadia"
print(r)


a = """Lorem ipsum dolor sit amet,
consectetur adipiscing elit,
sed do eiusmod tempor incididunt
ut labore et dolore magna aliqua."""
print(a)



a = '''Lorem ipsum dolor sit amet,
consectetur adipiscing elit,
sed do eiusmod tempor incididunt
ut labore et dolore magna aliqua.'''
print(a)


h="cpc python"
print(h[0])

print(h[-3:])


##loops
h="cpc python"
for element in h:
    print(element)


sum=0
p="1234"
for x in p:
    
    c=int(x)
    sum=sum+c
    print("الحلقة",sum)

print("total sum:",sum)


##طول السلسة 
print(h,len(h))


txt = "The best things in life are free!"
print("free" in txt)

txt = "The best things in life are free!"
if "free" in txt:
  print("Yes, 'free' is present.")