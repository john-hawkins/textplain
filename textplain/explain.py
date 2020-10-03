"""
   This is the core textplain interface.

   The models passed into these functions are required to implement a single function called 'predict(x)'
   The function should take a pandas dataframe of features, and return an array with a single value per record.
   This value should be numeric and could represent a probability or scalar value being forecast.

"""
###################################################################################################################
def explain_predictions(model, dataset, column, params):
    return "No idea"

###################################################################################################################
def explain_prediction(model, record, column, params):
    return "No idea"



