year = int(input("Enter a Year : "))

if((year % 400 == 0) | (year % 100 != 0) & (year % 4 == 0)):
  print("Is a Leap Year") 
else:
  print("Not a Leap Year")  
