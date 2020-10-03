import tensorflow_datasets as tfds
import tensorflow as tf
import pandas as pd

##############################################################################################
# Pipeline Bert
#
# Train a text classifer using BERT

class PipelineBERT():

    BUFFER_SIZE = 10000
    BATCH_SIZE = 64

    def __init__(self):
        pass

    def fit(self, x, y):
        """
            This function expects a list of text data in x and a numpy array of target integers in y 
        """
         dataset = self.create_bert_training_data(x,y)

         self.history = self.model.fit(train_dataset, epochs=10)

         return self

    def create_bert_training_data(x,y):

        train_df_bert = pd.DataFrame({
            'id':range(len(x)),
            'label':y,
            'alpha':['a']*len(x),
            'text': x
        })
        return train_df_bert


    ###################################################################################################3
    def predict(self, x):
        if isinstance(x, str):
            return self.model.predict( self.encoder.encode(x) )
        else:
            return self.model.predict( encodeall(x) )


    ###################################################################################################3
    def save(path):
         self.model.save(path + 'tf_model.h5') 
         self.encoder.save_to_file(path + 'encoder.dat')



