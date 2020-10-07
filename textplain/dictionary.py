"""
   This module provides dictionaries to look up synonyms and antonyms
"""

from nltk.corpus import wordnet

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



