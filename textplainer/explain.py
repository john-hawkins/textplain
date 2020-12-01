"""
   This is the core textplainer interface.

   The models passed into these functions are required to implement a single function called 'predict(x)'
   The function should take a pandas dataframe of features, and return an array with a single value per record.
   This value should be numeric and could represent a probability or scalar value being forecast.

"""
import re
import pandas as pd

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
    if impact == 0:
        # We have a text field that does not change the prediction from an empty string
        # Do not waste time analysing this any further
        return impact, record[column].values[0]
    else:
        # Deeper analysis
        return impact, deeper_explanation(model, record, column, baseline_score, null_score, params)


###################################################################################################################
def deeper_explanation(model, record, column, baseline, nullscore, params):
    textvalue = record[column].values[0]
    impact = baseline - nullscore
    sentences = re.split( "[.?!\n]", textvalue )
    sentences = [x.strip() for x in sentences]
    if "" in sentences:
        sentences.remove("")
    res = [] 
    [res.append(x) for x in sentences if x not in res] 
    # Generate a list of all variations removing each unique sentence
    # Tried this. But it creates the problem of reconstruction the punctuation that joined sentences
    # [[x for i,x in enumerate(test) if i!=j] for j in range(len(test))] 

    # This version will leave all original punctuation in place
    test_strings = [ textvalue.replace(x,"") for i,x in enumerate(sentences)]

    df_repeated = pd.concat([record]*len(test_strings), ignore_index=True)
    df_repeated[column] = test_strings

    sentence_scores = model.predict(df_repeated)
    # Calculate difference relative to the baseline
    impacts = baseline - sentence_scores
    result = textvalue
    for i,x in enumerate(sentences):
        result = result.replace(x, x + "{{" + str(impacts[i]) + "}}")

    return result


