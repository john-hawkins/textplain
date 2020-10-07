"""
   This is the core textplainer interface.

   The models passed into these functions are required to implement a single function called 'predict(x)'
   The function should take a pandas dataframe of features, and return an array with a single value per record.
   This value should be numeric and could represent a probability or scalar value being forecast.

"""

###################################################################################################################

def explain_predictions(model, dataset, column, params):

    if str(type(column)) != "<class 'str'>":
        raise Exception("ERROR: Column name must be a string") 

    if 'predict' not in dir(model):
        raise Exception("ERROR: Model does not implement function 'predict'") 

    if column not in dataset.columns:
        raise Exception("ERROR: Dataset does not contain column: " + column) 

    rez = [] 
    for index, record in dataset.iterrows():
        rez.append(explain_prediction(model, record, column, params))
    return rez

###################################################################################################################

def explain_prediction(model, record, column, params):
    return record[column]


