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

