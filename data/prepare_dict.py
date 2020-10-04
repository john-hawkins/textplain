import pandas as pd

dict_file = "51155-0.txt2"
dictionary = {}
CURRENT_KEY = ""
process_started = False
antonyms_started = False
end_string ="End of the Project Gutenberg EBook"


##################################################################
def initialise_new_record(content):
    global CURRENT_KEY
    global antonyms_started
    CURRENT_KEY = content 
    antonyms_started = False
    dictionary[CURRENT_KEY] = {"SYN":[],"ANT":[]}

##################################################################
def finalise():
    print(dictionary)
    exit(1)

##################################################################
def update_content(starter, content, stripped_line):
    if  starter == "SYN:":
        update_synonyms(content)
    elif  starter == "ANT:":
        update_antonyms(content)
    else:
        if content.find(end_string) >=0:
            finalise() 
        elif antonyms_started :
            update_antonyms(stripped_line)
        else:
            update_synonyms(stripped_line)


##################################################################
def update_synonyms(content):
    update_dictionary(content,"SYN")

##################################################################
def update_antonyms(content):
    global antonyms_started
    antonyms_started = True
    update_dictionary(content,"ANT")

##################################################################
def update_dictionary(content,section):
    record = dictionary[CURRENT_KEY]
    newwds = content.split(",")
    newwds = list(map(str.strip,newwds))
    curr = record[section]
    curr.extend(newwds)
    record[section] = curr
    dictionary[CURRENT_KEY] = record


##################################################################

with open(dict_file, "r") as f:
    for line in f:
        print("PROCESSING:", line)
        stripped_line = line.strip()
        starter = stripped_line[0:4]
        content = stripped_line[5:]
        if starter == "KEY:":
            process_started = True
            initialise_new_record(content)
        elif process_started:
            update_content(starter, content, stripped_line)
    # NOW SAVE THE GENERATED DATA STRUCTURE
    finalise()
