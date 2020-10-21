import pandas as pd
import numpy as np

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
        self.freqs = build_word_dictionary(df, text, label)

        X = np.zeros((len(df), 3))
        for i in range(len(df)):
            X[i, :]= extract_features(df[text][i], self.freqs)

        Y = df[label] 

        J, self.theta = gradientDescent(X, Y, np.zeros((3, 1)), 1e-9, 1500)
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

