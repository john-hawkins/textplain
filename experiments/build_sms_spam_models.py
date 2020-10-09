import pandas as pd
import numpy as np

import Pipeline_Sklearn_NGram_Tfidf_SGD_Classifier as p1
import Pipeline_TensorFlow_Subword_Bidirec_LSTM_Classfier as p2

df = pd.read_csv("../data/smsspam/SMSSpamCollection", sep="\t", header=None)

df.columns=['label','text']
df['label'] = np.where(df['label']=="spam",1,0)

samples = len(df)
temp = list(range(0, 10))
temp.extend(list(range(samples-10,samples)))

test_set = df.index.isin(temp)
test = df[test_set]
train = df[~test_set]

y = np.array(train['label'])
x = train['text'].tolist()

pipe1 = p1.Pipeline_Sklearn_NGram_Tfidf_SGD_Classifier()
model = pipe1.fit(x,y)

pipe2 = p2.Pipeline_TensorFlow_Subword_Bidirec_LSTM_Classfier()
model2 = pipe2.fit(x,y)

