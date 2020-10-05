#!/bin/bash

wget http://www.gutenberg.org/files/51155/51155-0.txt

# THERE ARE 34073 LINES
# OF WHICH THE FIRST 98 ARE INTRO
tail -n 33975 51155-0.txt > temp.txt
# AND THE FINAL XX ARE OUTRO
head -n 33608 temp.csv > data.txt
rm temp.txt

#python prepare_dict.py

