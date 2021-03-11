"""
   Test Models

   A set of trivial models for PyTests
"""

import pandas as pd
import numpy as np
import re

class SingleWordModel:

    def __init__(self, name, colname, myword):
        self.name = name
        self.colname = colname
        self.word = myword
 
    def predict(self, x: pd.DataFrame) -> np.ndarray:
        #if len(x) > 1:
        #    rez = np.where( x[self.colname].str.find(self.word)>=0,1,0)
        #else:
        #    rez = np.where( x[self.colname].find(self.word)>=0,1,0)    
        rez = np.where( x[self.colname].str.find(self.word)>=0,1,0)
        return rez


class MultiWordModel:

    def __init__(self, name, colname, mywords):
        self.name = name
        self.colname = colname
        self.words = mywords

    def predict(self, x: pd.DataFrame) -> np.ndarray:
        score = 0
        for w in self.words:
            score += np.where( x[self.colname].str.find(w)>=0,1,0)
        score = score/len(self.words)
        return score

