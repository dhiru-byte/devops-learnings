#! /usr/bin/python

import os
import sys
import glob


#To List All files with .feature extension
os.chdir("/root/python")
for file in glob.glob("*.feature"):

#Printing the name of all files with required extension
    print(file)
    
#read input file
fin = open("first.feature", "rt")
#read file contents to string
data = fin.read()
#replace all occurrences of the required string
data = data.replace('TM-13657 ', 'TM-1')
#close the input file
fin.close()
#open the input file in write mode
fin = open("first.feature", "wt")
#overrite the input file with the resulting data
fin.write(data)
#close the file
fin.close()    
      
      
      
      
#def find_file(file_name, directory_name):
#    files_found = []
#    for path, subdirs, files in os.walk(directory_name):
#        for name in files:
#            if(file_name == name):
#                file_path = os.path.join(path,name)
#                files_found.append(file_path)
#    return files_found
#find_file('test.txt', '/root/python')

