#!/bin/bash

# The input file needs to contain Big5 codes for the characters whose stroke order info is wanted, line by line.

FILE=big5.txt

while read line; do
     wget http://stroke-order.learningweb.moe.edu.tw/words/$line.png
     echo "Got it : $line"
done < $FILE

exit