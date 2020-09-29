from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from pprint import pprint
from time import time 
import pandas as pd

##############################################################################################
# PipelineOne
#
# Our first ML Pipeline. We use the same overall class structure in all examples

class PipelineOne():

    pipeline = Pipeline([
        ('vect', CountVectorizer()),
        ('tfidf', TfidfTransformer()),
        ('clf', SGDClassifier(loss='log')),
    ])

    parameters = {
        'vect__max_df': (0.5, 0.75, 1.0),
        'vect__ngram_range': ((1, 1), (1, 2)),  # unigrams or bigrams
        'clf__max_iter': (20,),
        'clf__alpha': (0.00001, 0.000001),
        'clf__penalty': ('l2', 'elasticnet'),
    }

    def __init__(self):
        pass

    def fit(self, x, y):
        """
            This function expects a list of text data in x and a numpy array of target integers in y 
        """
 
        grid_search = GridSearchCV(self.pipeline, self.parameters, n_jobs=-1, verbose=1)

        print("Performing grid search...")
        print("pipeline:", [name for name, _ in self.pipeline.steps])
        print("parameters:")
        pprint(self.parameters)
        t0 = time()
        grid_search.fit(x, y)
        print("done in %0.3fs" % (time() - t0))
        print()

        print("Best score: %0.3f" % grid_search.best_score_)
        print("Best parameters set:")
        best_parameters = grid_search.best_estimator_.get_params()
        for param_name in sorted(self.parameters.keys()):
            print("\t%s: %r" % (param_name, best_parameters[param_name]))

        self.model = grid_search.best_estimator_

        return self.model

    def predict(self, x):
        return self.model.predict_proba(x)


