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
        # NOTE: We can't use the record directly because pandas produces a Series object
        # in this form of iteration. We need to use the trick below to force it to produce
        # a single record DataFrame
        rez.append(explain_prediction(model, dataset.loc[index:index], column, params))

    return rez

###################################################################################################################

def explain_prediction(model, record, column, params):
    baseline_score = model.predict(record)[0]
    null_record = record.copy()
    null_record[column] = ""
    null_score = model.predict(null_record)[0]
    impact = baseline_score - null_score 
    #print("impact: ", impact, " type:", type(impact))
    return impact, record[column].values[0]


