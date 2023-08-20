# num = input("Enter the number : ")
# sum = int(num[0]) + int(num[1])
# print(sum)

num = input("Enter the number : ")

sum = 0
for digit in str(num):
 sum += int(digit)
print(sum)

