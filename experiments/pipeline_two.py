from __future__ import absolute_import, division, print_function, unicode_literals

import tensorflow_datasets as tfds
import tensorflow as tf
import pandas as pd

##############################################################################################
# PipelineOne
#
# Second ML Pipeline. 
# TensorFlow Bi-Direction LSTM

class PipelineTwo():

    BUFFER_SIZE = 10000
    BATCH_SIZE = 64

    def __init__(self):
        pass

    def fit(self, x, y):
        """
            This function expects a list of text data in x and a numpy array of target integers in y 
        """
         gen = (n for n in x)
         self.encoder = tfds.features.text.SubwordTextEncoder.build_from_corpus(gen, target_vocab_size=10000)

         tempy = pd.DataFrame({'text':x})
         dataset = tf.data.Dataset.from_tensor_slices((tempy.values, y))

         def encode(text_tensor, label):
             encoded_text = self.encoder.encode(text_tensor.numpy())
             return encoded_text, label

         def encode_map_fn(feats, label):
             text = feats[0]
             encoded_text, label = tf.py_function(encode,inp=[text, label],Tout=(tf.int64, tf.int64)
             # tf.data.Datasets work best if all components have a shape set
             encoded_text.set_shape([None])
             label.set_shape([])
             return encoded_text, label

         encoded_dataset = dataset.map(encode_map_fn)

         train_dataset = encoded_dataset.shuffle(self.BUFFER_SIZE)
         output_shapes = tf.compat.v1.data.get_output_shapes(train_dataset)

         self.model = tf.keras.Sequential([
             tf.keras.layers.Embedding(encoder.vocab_size, 64),
             tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64)),
             tf.keras.layers.Dense(64, activation='relu'),
             tf.keras.layers.Dense(1, activation='sigmoid')
         ])

         self.model.compile(loss='binary_crossentropy',
              optimizer=tf.keras.optimizers.Adam(1e-4),
              metrics=['accuracy'])

         self.history = self.model.fit(train_dataset, epochs=10)

         return self

    ###################################################################################################3
    def predict(self, x):
        if isinstance(x, str):
            return self.model.predict( self.encoder.encode(x) )
        else:
            return self.model.predict( encodeall(x) )

    ###################################################################################################3
    def encode_all(self, x):
        """
           This function will take an array of text and prepare it so that they can be all scored by the
           model in parrallel. This means encoding them and then padding them to have the same length.
        """
        enc1 = list( map(self.encoder.encode, x) )
        maxlen = max(map(len,enc1))
        def custom_pad(e):
            out = [0] * maxlen
            out[:len(e)] = e
            return out
        enc2 = list( map(custom_pad,enc1) )
        return enc2


    ###################################################################################################3
    def save(self, path):
         self.model.save(path + 'tf_model.h5') 
         self.encoder.save_to_file(path + 'encoder.dat')



