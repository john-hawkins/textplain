import pandas as pd
import re

dict_file = "temp.txt"
#dict_file = "data2.txt"
dictionary = {}
CURRENT_KEY = ""
process_started = False
antonyms_started = False

# Some entries contain multiple words that should have independent entries
# For the moment we will use the first key
key_split_pattern = " or "

# NOTES
# There are multiple keys that contain phrasal verbs, or additonal grammatical
# notes in the key field. We are ignoring them for the moment which will render
# the corresponding entry inaccessible by word look up. There are 20 odd entries
# like this. E.g carry on, fawn upon, pluck up

##################################################################
def initialise_new_record(content):
    global CURRENT_KEY
    global antonyms_started
    mykey, ref, pos = extract_key_ref_pos(content)
    if len(mykey.split(key_split_pattern))>1:
        mykey = mykey.split(key_split_pattern)[0]
    if pos == "":
        pos = 'x'
    CURRENT_KEY = mykey + "_" + pos 
    antonyms_started = False
    dictionary[CURRENT_KEY] = {"SYN":[], "ANT":[], "REF":ref, "POS":pos}


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
        if antonyms_started :
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
    if "" in newwds:
        newwds.remove("")
    curr = record[section]
    curr.extend(newwds)
    record[section] = curr
    dictionary[CURRENT_KEY] = record


##################################################################
def extract_key_ref_pos(content):
    pos = ""
    refs = []
    res = re.findall(r"\\[a-zA-Z]+\.?\\", content)
    if len(res) != 0:
        pos = res[0]
        pos = pos[1]
    temp = re.sub(r"\\[a-zA-Z]+\.?\\", '', content).strip()
    res = re.findall(r"\[[^\]]*\]", temp)
    for r in res:
        ref = re.sub(r"\[see", '', r, flags=re.IGNORECASE).strip()
        ref = re.sub(r"\]", '', ref).strip()
        refl = ref.split(" and ")
        refs.extend(refl)
    keys = re.sub(r"\[.*\]", '', temp).strip()
    new_key = keys.split(",")[0].strip()
    if len(new_key) == 0:
        if len(refs) > 0:
           new_key = refs[0]
    return new_key, refs, pos


##################################################################
def replace_refs(content):
    return re.sub(r"\[see (.*)\]", '\\1', content, flags=re.IGNORECASE).strip()


##################################################################
with open(dict_file, "r") as f:
    for line in f:
        #print("PROCESSING:", line)
        stripped_line = line.strip()
        stripped_line = clean(stripped_line)
        stripped_line = re.sub("_", ' ', stripped_line)
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




