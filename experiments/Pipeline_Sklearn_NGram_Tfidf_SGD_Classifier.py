from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from pprint import pprint
from time import time 
import pandas as pd
import numpy as np

##############################################################################################
# Pipeline_Sklearn_NGram_Tfidf_SGD_Classifier.
#
# A complete ML Pipeline for classifying text data.
#
# The fit function will train a model by applying the following stages
#  - Word Count Vectorization
#  - TFIDF Transformation
#  - SGD Linear Classifier
#

class Pipeline_Sklearn_NGram_Tfidf_SGD_Classifier():

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

    ###################################################################################################

    def __init__(self, results_dir):
        self.results_dir = results_dir

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


    ###################################################################################################

    def fit_from_vectors(self, x, y):
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

        return self

    ###################################################################################################

    def predict(self, df):
        """
            Given a DataFrame that has the required field from training, make predictions for
            each row.
        """
        x = df[self.text_col_name].tolist()
        return self.predict_from_vectors(x)

    ###################################################################################################

    def predict_from_vectors(self, x):
        return self.model.predict_proba(x)


    ###################################################################################################



