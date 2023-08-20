import random
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X','Y', 'Z']

number = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

special_char = ['!', '^', '$', '*', '&', '@', '(', ')', '%']

print("Password Generator")
alpha= int(input("How many alphabet : "))
num = int(input("How many number : "))
char = int(input("How many special Character : "))

password= ""
# for i in range (0, alpha):
# #  alpha_gen = random.choice(alphabet)
# #  password += alpha_gen
#  password += random.choice(alphabet)

# for i in range(0, num):
# #  num_gen = random.choice(number)
# #  password += num_gen
#  password += random.choice(number)

# for i in range(0, char):
# #  char_gen = random.choice(special_char)
# #  password += char_gen 
#  password += random.choice(special_char)
 
# print(password)

password_list = []
for i in range (0, alpha):
 password_list.append (random.choice(alphabet))

for i in range (0, num):
 password_list.append (random.choice(number))

for i in range (0, char):
 password_list.append (random.choice(special_char))

random.shuffle(password_list)
print(password_list)

for i in  password_list:
 password += i
print("your password : " + password) 