import tensorflow_datasets as tfds
import tensorflow as tf
import pandas as pd
import numpy as np

##############################################################################################
# Pipeline_TensorFlow_Subword_Bidirec_LSTM_Classfier
#
# TensorFlow Bi-Direction LSTM Model for Classifying Text data
# This pipeline 

class Pipeline_TensorFlow_Subword_Bidirec_LSTM_Classfier():

    BUFFER_SIZE = 10000
    BATCH_SIZE = 64

    def __init__(self):
        pass


    ###################################################################################################

    def fit(self, df, text, label):
        """
            This function expects a pandas dataframe and two strings that determine the names of
            of the text features column and the target column. From this, we will build a model.
        """
        self.text_col_name = text
        self.label_col_name = label
        y = np.array(df[label])
        x = df[text].tolist()
        return self.fit_from_vectors(x, y)


    def fit_from_vectors(self, x, y):
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
             encoded_text, label = tf.py_function(encode,inp=[text, label],Tout=(tf.int64, tf.int64))
             encoded_text.set_shape([None]) # tf.data.Datasets work better with a shape set
             label.set_shape([])
             return encoded_text, label

        encoded_dataset = dataset.map(encode_map_fn)

        train_dataset = encoded_dataset.shuffle(self.BUFFER_SIZE)
        output_shapes = tf.compat.v1.data.get_output_shapes(train_dataset)
        train_dataset = train_dataset.padded_batch(self.BATCH_SIZE, output_shapes)

        self.model = tf.keras.Sequential([
             tf.keras.layers.Embedding(self.encoder.vocab_size, 64),
             tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64)),
             tf.keras.layers.Dense(64, activation='relu'),
             tf.keras.layers.Dense(1, activation='sigmoid')
        ])

        self.model.compile(loss='binary_crossentropy',
              optimizer=tf.keras.optimizers.Adam(1e-4),
              metrics=['accuracy'])

        self.history = self.model.fit(train_dataset, epochs=10)

        return self

    ###################################################################################################

    def predict(self, df):
        """
            Given a DataFrame that has the required field from training, make predictions for
            each row.
        """
        x = df[self.text_col_name].tolist()
        return self.predict_from_vectors(x)

    ###################################################################################################3
    def predict_from_vectors(self, x):
        encoded = []
        if isinstance(x, str):
            encoded.append(self.encoder.encode(x))
            return self.model.predict(encoded)
        else:
            return self.model.predict(self.encode_all(x))


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

