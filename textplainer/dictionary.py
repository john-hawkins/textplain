"""
   This module provides dictionaries to look up synonyms and antonyms
"""
# -*- coding: utf-8 -*-

from .process import eprint

try:
   from nltk.corpus import wordnet
   NLTKWORDNET = True
except:
   eprint(" * WARNING: The complete synonym dictionary requires the wordnet corpus : nltk.download('wordnet') ")
   NLTKWORDNET = False

###################################################################################################################

def get_synonyms_and_antonyms(word):
    """
        Entry function to obtain a list of synonyms and antonyms for a given word.
        This function will rely on other libraries and datasets and merge them for 
        a comprehensive reference.
    """
    if NLTKWORDNET:
        syns, ants = get_nltk_synonyms_and_antonyms(word)
    else:
        syns, ants = ["test"], ["test"]
    return syns, ants

###################################################################################################################

def get_nltk_synonyms_and_antonyms(word):
    synonyms = []
    antonyms = []
    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            synonyms.append(l.name())
            if l.antonyms():
                antonyms.append(l.antonyms()[0].name())
    synonyms = list(set(synonyms))
    antonyms = list(set(antonyms))
    if word in synonyms:
        synonyms.remove(word)
    if word in antonyms:
        antonyms.remove(word)
    return synonyms,antonyms

###################################################################################################################

def get_fallows_synonyms_and_antonyms(word):
    return [],[]

