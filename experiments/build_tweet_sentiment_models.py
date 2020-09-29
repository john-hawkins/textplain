import pandas as pd
import numpy as np
import pipeline_one as p1

df = pd.read_csv("../data/Sentiment140/training.1600000.processed.noemoticon.csv", header=None, encoding = "ISO-8859-1")

df.columns = ['polarity','id','date','query','user','text']
df['label'] = np.where(df['polarity']==4,1,0)

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

