"""
   ModelInterface

   This class illustrates what a model needs to implement in order to function
   with textplain. The key is simply a predict function that can operate on a 
   pandas dataframe and return an array of scalar results equal in length to the
   dataframe. 

   In other words, the outpout should be a single number for every record in the
   data being tested. This could be the probability of the positive class for binary
   prediction, BUT NOT the vector of class probabilities.

   For examples of post-processing for common models and ML framewords see the 
   pipelines in the directory of experiments.
"""

import pandas as pd
import numpy as np

class ModelInterface:

    def __init__(self, name):
        self.name = name


    def predict(self, x: pd.DataFrame) -> np.ndarray:
        return np.zeros(len(x)) 


