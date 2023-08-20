names = []                                   ### Empty List Create
n = int(input("Enter No. of Elements : "))   ### Number of element you want to input.

for i in range(0, n):                        ### for loop from 0 to n entered. 
   x = str(input())                          ### Take input of ith element as x.
   names.append(x)                           ### Append the element to names list. 
print(names)