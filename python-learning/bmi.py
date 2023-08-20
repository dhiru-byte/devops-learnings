weight = int(input("Enter  Weight  in KG : "))
height = float(input("Enter Height in Meter M : "))
bmi = weight/(height**2)

print(bmi)
print("Your BMI: ", round(bmi, 2))

if bmi < 18.5 :
 print("You are Skinny pete")  
elif ((bmi > 18.5) & (bmi < 25 )):
 print("You have Normal Weight")
elif ((bmi > 25) & (bmi < 30)):
 print("You are Overweight")
elif ((bmi > 30 ) & (bmi < 35)):
 print("You are Obese")  
elif (bmi > 35):
 print("Need to do Something")
   