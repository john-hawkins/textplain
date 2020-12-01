import pandas as pd
import numpy as np
import math

##############################################################################################
# Pipeline_Simple_WordLabel_Count_LogisticReg 
#
# A Simple ML Pipeline for classifying text data.
#
# The fit function will train a model by applying the following stages
#  - Word Counts by Label Dictionary
#  - Simple Logistic Regression on Sums of Positive and Negative Class Words
#

class Pipeline_Simple_WordLabel_Count_LogisticReg():


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

        X = np.zeros((len(df), 3))
        i = 0
        for index, row in df.iterrows():
            X[i, :]= self.extract_features(row[text], self.freqs)
            i = i + 1

        Y = df[label].to_numpy()
        Y.shape = (len(Y),1)

        J, self.theta = self.gradientDescent(X, Y, np.zeros((3, 1)), 1e-7, 1005000)
        print(f"The cost after training is {J:.8f}.")
        print(f"The resulting vector of weights is {[round(t, 8) for t in np.squeeze(self.theta)]}")

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

    def sigmoid(self, z): 
        '''
        Input:
            z: is the input (can be a scalar or an array)
        Output:
            h: the sigmoid of z
        '''  
        def sigm(inp):
            return 1/(1 + math.exp(-inp))
        vsigm = np.vectorize(sigm)
        x = np.asarray(z)
        scalar_input = False
        if x.ndim == 0:
            x = x[None]  # Makes x 1D
            scalar_input = True
        ret = vsigm(x)
        if scalar_input:
            h = np.squeeze(ret)
        else:
            h = ret
        return np.array(h)
    
    
    ###################################################################################################
    def gradientDescent(self, x, y, theta, alpha, num_iters):
        '''
        Input:
            x: matrix of features which is (m,n+1)
            y: corresponding labels of the input matrix x, dimensions (m,1)
            theta: weight vector of dimension (n+1,1)
            alpha: learning rate
            num_iters: number of iterations you want to train your model for
        Output:
            J: the final cost
            theta: your final weight vector
        Hint: you might want to print the cost to make sure that it is going down.
        '''
        m = None
        lowest_cost = np.inf
        best_theta = theta        
        for i in range(0, num_iters):
            
            z = np.dot(x, theta)
            
            h = self.sigmoid(z)
            
            def cost(ys, preds):
                logpreds = np.log(preds)
                logonempreds = np.log(1-preds)
                pt1 = np.dot(np.transpose(ys), logpreds)
                pt2 = np.dot(np.transpose(1-ys), logonempreds)
                return -(pt1+pt2)/len(ys)
            
            J = cost(y,h)
    
            def theta_delta(xs, ys, preds):
                return np.dot( np.transpose(xs), (preds-ys) ) / len(ys)
            if J < lowest_cost:
                lowest_cost = J
                best_theta = theta
            elif lowest_cost < (J*1.05):
                print(f"Applying early stopping after {i} rounds") 
                return float(lowest_cost), best_theta

            theta = theta - alpha*theta_delta(x, y, h)
            
        J = float(J)
        return J, theta
    
    
    ###################################################################################################
    def extract_features(self, text, freqs):
        '''
        Input: 
            text: a list of words for one text
            freqs: a dictionary corresponding to the frequencies of each tuple (word, label)
        Output: 
            x: a feature vector of dimension (1,3)
        '''
        # process_text tokenizes, stems, and removes stopwords
        word_l = self.process_text(text)
        # 3 elements in the form of a 1 x 3 vector
        x = np.zeros((1, 3)) 
        #bias term is set to 1
        x[0,0] = 1 
        # loop through each word in the list of words
        for word in word_l:
            # increment the word count for the positive label 1
            x[0,1] += freqs.get( (word, 1.0), 0)
            # increment the word count for the negative label 0
            x[0,2] += freqs.get( (word, 0.0), 0)
            
        return x
    
    ###################################################################################################
    def process_text(self, text):
        #tweet2 = re.sub(r'https?:\/\/.*[\r\n]*', '', tweet2)
        #!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
        stop_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]
        return text.split()
    
    ###################################################################################################
    def predict_text(self, text, freqs, theta):
        '''
        Input: 
            text: a string
            freqs: a dictionary corresponding to the frequencies of each tuple (word, label)
            theta: (3,1) vector of weights
        Output: 
            y_pred: the probability of a text being positive or negative
        '''
        x = self.extract_features(text, freqs)
        z = np.dot(x, theta)
        y_pred = self.sigmoid(z)
        return y_pred

