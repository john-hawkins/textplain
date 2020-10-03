import pandas as pd

dict_file = "51155-0.txt2"

dictionary = {}

CURRENT_KEY = ""
antonyms_started = False
end_string ="End of the Project Gutenberg EBook"

with open(dict_file, "r") as f:
  for line in f:
    stripped_line = line.strip()
    starter = stripped_line[0:4]
    content = stripped_line[5:]
    if starter == "KEY:"
        initialise_new_record(content)
    else 
        update_content(starter, content, stripped_line)


def initialise_new_record(content):
    CURRENT_KEY = content 
    antonyms_started = False


update_content(starter, content, stripped_line):
    if  starter == "SYN:"
        update_synonyms(content)
    elif  starter == "ANT:"
        update_antonyms(content)
    elif antonyms_started :
        update_antonyms(stripped_line)
    else:
        update_synonyms(stripped_line)


def update_synonyms(content):




def update_antonyms(content):
    antonyms_started = True





