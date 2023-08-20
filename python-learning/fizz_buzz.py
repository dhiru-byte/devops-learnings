for i in range(1, 50):
 if(i%3==0 and i%5==0):   #print "Fizz Buzz" if number is divisible by both 3 & 5
  print("Fizz Buzz")

 elif (i%3==0):           #print "Fizz" if number is divisible by 3 only.
   print("Fizz")
   
 elif(i%5==0):            #print "Fizz" if number is divisible by 5 only.
   print("Buzz")
   
 else:                   #print number if above conditions false.
   print(i) 
