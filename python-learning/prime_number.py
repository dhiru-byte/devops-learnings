num = int(input("Enter A number: "))

if (num > 1):
 print("greater than 1")
 for i in range(2, int(num/2)+1):   ## for loop syntax in python using range from 2 to num/2 .
  if (num % i == 0):
     print("Complete Divisible")
     break     #break needed because on finding first Complete divisible number it won't be prime so need to break out of the for loop
 else:
     print("Prime Number") 
else:
  print("Not Prime")     

      
