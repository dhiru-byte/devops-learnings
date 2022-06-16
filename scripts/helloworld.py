#! /usr/bin/python

#Prepend #! /usr/bin/python with your script.

#Run the following command in your terminal to make the script executable: chmod +x SCRIPTNAME.py

#Now, ?simply type ./SCRIPTNAME.py to run the executable script.

msg = "Hello World"
print(msg)
print("Learning python")


# Python code to reverse a string  
# using loop 
  
def reverse(s): 
  str = "" 
  for i in s: 
    str = i + str
  return str
  
s = "Geeksforgeeks"
  
print ("The original string  is :") 
print (s) 
  
print ("The reversed string(using loops) is :") 
print (reverse(s)) 


txt = "Hello World" [::-1]
print(txt)


def my_function(x):
  return x[::-1]

mytxt = my_function("I wonder how this text looks like backwards")
f = open("test.txt")

test = my_function(f.read)
print(mytxt)
#f = open("test.txt")
print(f.read())
print(test)