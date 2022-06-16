#!/bin/bash

RANDOM=$$ 
num=0 
ARG=${1:-10} 
while [[ ${num} -le ${ARG} ]] 
do 
echo "$num, $RANDOM" >> inputFile
((num=num+1)) 
done
 