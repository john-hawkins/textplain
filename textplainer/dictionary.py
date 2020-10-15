"""
   This module provides dictionaries to look up synonyms and antonyms
"""
# -*- coding: utf-8 -*-

import nltk
import pickle
import pkg_resources

from .process import eprint

try:
   nltk.data.find('wordnet')
   from nltk.corpus import wordnet
   NLTKWORDNET = True
except:
   eprint(" * WARNING: The complete synonym dictionary requires the wordnet corpus : nltk.download('wordnet') ")
   NLTKWORDNET = False


########################################################################################
resource_package = __name__

def load_dictionary(filename):
    """
    Utility function to load pre-generated dictionary files
    """
    _path = '/'.join(('data', filename))
    rawd = pkg_resources.resource_string(resource_package, _path)   #.decode("utf-8")
    return pickle.loads(rawd)

fallows = load_dictionary("fallows.dat")

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

def get_fallows_synonyms_and_antonyms(word, pos='x'):
    """
        Get list of synonyms and antonyms from the digitised fallows dictionary.
        Will try to use POS specific entry if requested, otherwise fallback to a
        generic entry.
    """
    syns = []
    ants = []
    temp_key = word.lower() + "_" + pos.lower()
    if temp_key in fallows:
        entry = fallows[temp_key]
        syns.extend(entry['SYN'])
        ants.extend(entry['ANT'])
    elif pos != 'x':
        temp_key = word.lower() + "_x"
        if temp_key in fallows:
            entry = fallows[temp_key]
            syns.extend(entry['SYN'])
            ants.extend(entry['ANT'])
    return syns, ants

