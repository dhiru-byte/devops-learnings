strg = str(input("Enter a String : ")).lower()    ### lower function in python to convert the entered string in lower case to include the occurence of albhabet if there is any Upper case occurence of a particular character. 

print(strg.count("d") )             ### Count the occurence of a character .
print(strg.upper())                 ### Converts the string to Uppercase.
print(strg.lower())                 ### Converts the string to lowercase.
print(len(strg))                    ### Returns the length of the string.
print(strg.capitalize())            ### Converts the first character of the string to uppercase and the rest to lowercase.
print(strg.title())                 ### Converts the first character of each word in the string to uppercase.
print(strg.strip())                 ### Removes leading and trailing whitespace characters from the string.
print(strg.split(","))              ### Splits the string into a list of substrings based on a delimiter.
print(",".join(strg))               ### Joins elements of a list into a single string using a specified separator.
print(strg.find("world"))           ### Returns the index of the first occurrence of a substring (or -1 if not found).
print(strg.replace("hello", "hi"))  ### Replaces all occurrences of a substring with a new string.
print(strg.startswith("hello"))     ###  Checks if the string starts with a specified substring. 
print(strg.endswith("world"))       ###  Checks if the string ends with a specified substring.