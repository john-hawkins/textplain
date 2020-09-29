import pandas as pd
import numpy as np

import pipeline_one as p1

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

pipe1 = p1.PipelineOne()
model = pipe1.fit(x,y)


y = np.array(df['label'])
x = df['text'].tolist()

pipe1_sms = p1.PipelineOne()
model_sms = pipe1_sms.fit(x,y)

