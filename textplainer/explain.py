import re
import pandas as pd

from .dictionary import get_synonyms_and_antonyms

"""
   This is the core textplainer interface.

   The models passed into these functions are required to implement a 
   single function called 'predict(x)'
   The function should take a pandas dataframe of features, and return 
   an array with a single value per record.
   This value should be numeric and could represent a probability or 
   scalar value being forecast.
   The module will use changes in the magnitude of this value as an indicator
   of changed contribution by the features of the model.
"""

##################################################################################

def explain_predictions(model, dataset, column, params={}):
    """
    Explain the text data contributions to predictions made by the 
    given model on the provided dataset.

    :param model: The model to explain.
    :type model: Model object, required

    :param dataset: The dataset upon which to generate explanations of predictions.
    :type dataset: <class 'pandas.core.frame.DataFrame'>, required

    :param column: The name of the column in the dataset containing the text data to analyse.
    :type column: string, required

    :param params: Placeholer for additional paramaters that will control output.
    :type params: dictionary, optional

    :return: Return explanations as an Array with one entry per record.
    :rtype: Array( Tuple(Int, String) )
    """

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

##################################################################################

def explain_prediction(model, record, column, params={}):
    print(type(record))
    """
    Explain an individual record in terms of the contributions made by a specific
    column of text data within that record. We look at the predictions made by the
    given model on the provided dataset.

    :param model: The model to explain.
    :type model: Model object, required

    :param record: The record upon which to generate explanations of predictions.
    :type record: <class 'pandas.core.series.Series'>, required

    :param column: The name of the column in the dataset containing the text data to analyse.
    :type column: string, required

    :param params: Placeholer for additional paramaters that will control output.
    :type params: dictionary, optional

    :return: A tuple containg the following:
       * The estimated overall impact of the text data
       * A string describing the elements of the text that contribute to the prediction  
    :rtype: Tuple(Int, String)
    """

    baseline_score = model.predict(record)[0]
    null_record = record.copy()
    null_record[column] = ""
    null_score = model.predict(null_record)[0]
    impact = baseline_score - null_score 
    if impact == 0:
        # We have a text field that does not change the prediction from an empty string
        # Do not waste time analysing this any further
        # TODO: Parameterize this threshold
        return impact, record[column].values[0]
    else:
        # The impact is non-zero so do further analysis. Deeper analysis
        return impact, deeper_explanation(
            model, record, column, 
            baseline_score, null_score, params
        )


##################################################################################

def deeper_explanation(model, record, column, baseline, nullscore, params):
    """
    This function is called once we have established that the text data is contributing
    to the model outcome. We now investigate what it is about the text that makes that
    contribution.

    :param model: The model to explain.
    :type model: Model object, required

    :param record: The record upon which to generate explanations of predictions.
    :type record: <class 'pandas.core.series.Series'>, required

    :param column: The name of the column in the dataset containing the text data to analyse.
    :type column: string, required

    :param baseline: The baseline score of the record.
    :type baseline: float, required

    :param nullscore: The score of the record with the text removed
    :type nullscore: float, required

    :param params: Placeholer for additional paramaters that will control output.
    :type params: dictionary, optional

    :return: A string describing the elements of the text that contribute to the prediction
    :rtype: String
    """
    textvalue = record[column].values[0]
    impact = baseline - nullscore
    sentences = re.split( "[.?!\n]", textvalue )
    sentences = [x.strip() for x in sentences]
    if "" in sentences:
        sentences.remove("")
    res = [] 
    [res.append(x) for x in sentences if x not in res] 
    ###########################################################################
    # Generate a list of all variations removing each unique sentence
    # INITIAL ATTEMPT 
    # test_strings = [[x for i,x in enumerate(test) if i!=j] for j in range(len(test))] 
    # Created a downstream problem:
    # 'How to reconstruct the sequence of punctuation that joined sentences'
    # CURRENT VERSION
    # Will leave all original punctuation in place. 
    # It will mean that the text used in testing contains messy remnants of punctuation.
    # But we can be sure it is only testing the effect of the specific sentence removal.
    ###########################################################################
    test_strings = [ textvalue.replace(x,"") for i,x in enumerate(sentences)]

    df_repeated = pd.concat([record]*len(test_strings), ignore_index=True)
    df_repeated[column] = test_strings

    sentence_scores = model.predict(df_repeated)
    # Calculate difference relative to the baseline
    impacts = baseline - sentence_scores
    result = textvalue
    results_set = [] 
    for i, x in enumerate(sentences):
        sentence_impact = impacts[i]
        results_set.append( (i, x, sentence_impact) )
        # If the sentence has an impact then we investigate further
        # and replace the sentence with the explanatory sentence 
        # derived from further analysis
        if sentence_impact > 0:
            sntce_expl = sentence_explanation(
                model, record, column, 
                baseline, nullscore, x, sentence_impact,
                params)
            result = result.replace(x, sntce_expl)

    return result

##################################################################################
def sentence_explanation(model, record, column, baseline, nullscore, sentence, impact, params):
    """
    In this function we perform the final level of text contribution testing.
    We want to determine which words contribute most to the prediction, and what
    it is about the nature of those words. To do this we will substitute words with
    replacements from a dictionary of synonyms and antonyms.

    :param model: The model to explain.
    :type model: Model object, required

    :param record: The record upon which to generate explanations of predictions.
    :type record: <class 'pandas.core.series.Series'>, required

    :param column: The name of the column in the dataset containing the text data to analyse.
    :type column: string, required

    :param baseline: The baseline score of the record.
    :type baseline: float, required

    :param nullscore: The score of the record with the text removed
    :type nullscore: float, required

    :param sentence: The sentence from within the textfield we are explaining
    :type sentence: string, required

    :param impact: The previously determined impact of the text field on this record's score
    :type impact: float, required

    :param params: Placeholer for additional paramaters that will control output.
    :type params: dictionary, optional

    :return: A string describing the elements of the text that contribute to the prediction
    :rtype: String
    """
    # return sentence + "{{" + str(impact) + "}}"
    # Retrieve the synonyms an antonyms of all non-stop words
    textvalue = record[column].values[0]
    words = sentence.split(" ")
    syn_subs = []
    for i, w in enumerate(words):
        syns, ants = get_synonyms_and_antonyms(w)
        for s in syns: 
            syn_subs.append( (w, s, i) )
    if len(syn_subs)==0:
        result = sentence + "{{" + str(float(impact)) + "}}"
    else:
        df_synonyms = pd.concat([record] * len(syn_subs), ignore_index=True)
        replace_texts = []
        for i, x in enumerate(syn_subs):
            word_index = x[2]
            sub = x[1]
            rez=words.copy()
            rez[word_index]=sub
            new_sent = " ".join(rez)
            new_text = textvalue.replace(sentence, new_sent)
            replace_texts.append(new_text)
        df_synonyms[column] = replace_texts
        sentence_scores = model.predict(df_synonyms)
        impacts = baseline - sentence_scores

        expltns = {el:0 for el in words}
        current_word = words[0]
        count = 0
        total = 0
        for i, x in enumerate(syn_subs):
            this_word = x[0]
            if this_word != current_word:
                if count>0:
                    expltns[ current_word ] = total / count
                count = 0
                total = 0
                current_word = this_word
            total += impacts[i]
            count += 1
        expltns[ current_word ] = total / count
        # NOW THAT WE HAVE THE WORD LEVEL EXPLANATIONS
        # WE NEED TO INSERT THEM INTO THE TEXT
        result = sentence
        for w in words:
            print(w, " = ", expltns[w])
            if expltns[w]>0:
                result = result.replace(w, w + "{{" + str(expltns[w]) + "}}" )
    return result

