import pandas as pd
import numpy as np
import math

##############################################################################################
# Pipeline_Simple_NaiveBayes 
#
# A Simple ML Pipeline for classifying text data.
#
# The fit function will train a model by applying the following stages
#  - Naive Bayes built from the product of conditional probabilities of all words
#

class Pipeline_Simple_NaiveBayes():

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
        self.freqs = self.build_word_dictionary(df, text, label)
        train_y = df[self.label_col_name]
        self.logprior, self.loglikelihood = self.train_naive_bayes(self.freqs, train_y)

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
        """
            Given a list of text data, generate predictions for each record.
        """
        def predictor(text):
            return self.naive_bayes_predict(text, self.logprior, self.loglikelihood)

        return  

    ###################################################################################################

    def build_word_dictionary(self, df, text, label):
        freqs = {}
        for index, row in df.iterrows():
            word_l = self.process_text(row[text])
            lab = row[label]
            for word in word_l:
                key = (word, lab)
                val = freqs.get(key,0)
                freqs[key] = val + 1
        return freqs

    ###################################################################################################

    def train_naive_bayes(self, freqs, train_y):
        '''
        Input:
            freqs: dictionary from (word, label) to how often the word appears in each label set
            train_y: a list of labels correponding to the tweets (0,1)
        Output:
            logprior: the log prior. (equation 3 above)
            loglikelihood: the log likelihood of you Naive bayes equation. (equation 6 above)
        '''
        loglikelihood = {}
        logprior = 0
    
        # calculate V, the number of unique words in the vocabulary
        vocab = set([pair[0] for pair in freqs.keys()])
        V = len(vocab)
    
        # calculate N_pos and N_neg
        N_pos = N_neg = 0
        for pair in freqs.keys():
            # if the label is positive (greater than zero)
            if pair[1] > 0:
                # Increment the number of positive words by the count for this (word, label) pair
                N_pos += freqs[pair]
            # else, the label is negative
            else:
                # increment the number of negative words by the count for this (word,label) pair
                N_neg += freqs[pair]
    
        # Calculate D, the number of documents
        D = len(train_y)
    
        # Calculate D_pos, the number of positive documents 
        D_pos = sum(train_y)
    
        # Calculate D_neg, the number of negative documents 
        D_neg = D - D_pos
    
        # Calculate logprior
        logprior = np.log(D_pos) - np.log(D_neg)
    
        # For each word in the vocabulary...
        for word in vocab:
            # get the positive and negative frequency of the word
            freq_pos = freqs.get( (word,1), 0)
            freq_neg = freqs.get( (word,0), 0)
            # calculate the probability that each word is positive, and negative
            p_w_pos = (freq_pos + 1)/(N_pos + V)
            p_w_neg = (freq_neg + 1)/(N_neg + V)
            # calculate the log likelihood of the word
            loglikelihood[word] = np.log(p_w_pos/p_w_neg)
    
        return logprior, loglikelihood
  
    ###################################################################################################
    def process_text(self, text):
        #tweet2 = re.sub(r'https?:\/\/.*[\r\n]*', '', tweet2)
        #!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
        stop_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]
        return text.split()
    

    ###################################################################################################
    def naive_bayes_predict(self, text, logprior, loglikelihood):
        '''
        Input:
            text: a string
            logprior: a number
            loglikelihood: a dictionary of words mapping to numbers
        Output:
            p: the sum of all the logliklihoods of each word in the text (if found in the dictionary) + logprior (a number)
    
        '''
        word_l = self.process_text(text)
    
        # initialize probability to zero
        p = 0
    
        # add the logprior
        p += logprior
    
        for word in word_l:
    
            # check if the word exists in the loglikelihood dictionary
            if word in loglikelihood:
                # add the log likelihood of that word to the probability
                p += loglikelihood[word]
    
        return p


