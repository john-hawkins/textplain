import pandas as pd
import re

dict_file = "temp.txt"
dictionary = {}
CURRENT_KEY = ""
process_started = False
antonyms_started = False
end_string ="End of the Project Gutenberg EBook"


##################################################################
def initialise_new_record(content):
    global CURRENT_KEY
    global antonyms_started
    mykey, ref, pos = extract_ref_or_pos(content)
    CURRENT_KEY = mykey 
    antonyms_started = False
    dictionary[CURRENT_KEY] = {"SYN":[],"ANT":[],"REF":ref, "POS":pos}

##################################################################
def finalise():
    print(dictionary)
    exit(1)

##################################################################
def clean(x):
    temp = re.sub('\{\[(.*)\]\?\}', '\\1', x)    
    temp2 = re.sub('\.','',temp)
    temp3 = re.sub('=','',temp2)
    return temp3

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
def extract_ref_or_pos(content):
    pos = ""
    ref = ""
    res = re.findall(r"\\[a-zA-Z]+\.\\", content)
    if len(res) != 0:
        pos = res[0]
    temp = re.sub(r"\\[a-zA-Z]+\.\\", '', content).strip()
    res = re.findall(r"\[.*\]", temp)
    if len(res) != 0:
        ref = res[0]
        ref = re.sub(r"\[see", '', ref, flags=re.IGNORECASE).strip()
        ref = re.sub(r"\]", '', ref).strip()
    new_key = re.sub(r"\[.*\]", '', temp).strip()
    if len(new_key) == 0:
        new_key = ref
    return new_key, ref, pos


##################################################################
def replace_refs(content):
    return re.sub(r"\[see (.*)\]", '\\1', content, flags=re.IGNORECASE).strip()

##################################################################

with open(dict_file, "r") as f:
    for line in f:
        print("PROCESSING:", line)
        stripped_line = line.strip()
        stripped_line = clean(stripped_line)
        starter = stripped_line[0:4]
        content = stripped_line[5:]
        if starter == "KEY:":
            process_started = True
            initialise_new_record(content.lower())
        elif process_started:
            content = replace_refs(content).lower()
            stripped_line = replace_refs(stripped_line).lower()
            update_content(starter, content, stripped_line)
    # NOW SAVE THE GENERATED DATA STRUCTURE
    finalise()
