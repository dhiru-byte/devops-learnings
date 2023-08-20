age = int(input("Enter Your Age: "))

years_left = 90 - age
days_left = years_left * 365
weeks_left = years_left * 52
months_left = years_left * 12

print(years_left)
print(days_left)
print(weeks_left)
print(months_left)

print(f"You Have {days_left} days, {weeks_left} weeks, {months_left} months, {years_left} years left.")