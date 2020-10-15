#!/bin/bash

wget http://www.gutenberg.org/files/51155/51155-0.txt

# THERE ARE 34073 LINES IN THE RAW TEXT FILE
# OF WHICH THE FIRST 98 ARE INTRO
tail -n 33975 51155-0.txt > temp.txt

# AND THE FINAL 367 ARE OUTRO
head -n 33608 temp.csv > data.txt
rm temp.txt

# WE NOW HAVE THE DICTIONARY ENTRIES ONLY, BUT...
# We need to fix some of the format inconsistencies
sed 's/_SYN/\r\nSYN/g' data.txt > data2.txt



#python prepare_dict.py

