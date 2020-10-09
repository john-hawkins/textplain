import pandas as pd
import numpy as np
from textplainer.explain import explain_prediction
from textplainer.explain import explain_predictions
from textplainer.ModelInterface import ModelInterface
from textplainer.dictionary import get_synonyms_and_antonyms

def test_result_length():
    null_model = ModelInterface("NULL")
    df = pd.DataFrame({"id":[1,2,3],"text":["the cat","the hat","the mat"]})
    result = explain_predictions(null_model, df, "text", None)
    assert len(result) == len(df), "Explain function returns results for all records"

def test_dictionary():
    syns, ants = get_synonyms_and_antonyms("test")
    assert str(type(syns)) == "<class 'list'>", "Synonyms should be returned as a list"
    assert str(type(ants)) == "<class 'list'>", "Antonyms should be returned as a list"


def test_result_attributes():
    null_model = ModelInterface("NULL")
    df = pd.DataFrame({"id":[1,2],"text":["the cat","the hat"]})
    result = explain_predictions(null_model, df, "text", None)
    assert str(type(result)) == "<class 'list'>", "Explain function returns a list"
    assert str(type(result[0])) == "<class 'str'>", "Returned list contains strings"

def test_exceptions():
    null_model = ModelInterface("NULL")
    df = pd.DataFrame({"id":[1,2],"text":["the cat","the hat"]})
    thrown = False
    try:
        result = explain_predictions(null_model, df, 9, None)
    except:
        thrown = True
    assert thrown == True, "Exception should be thrown when column name is not a string"


    thrown = False
    try:
        result = explain_predictions(null_model, df, "textnot", None)
    except:
        thrown = True
    assert thrown == True, "Exception should be thrown when column is not present in dataframe"

    thrown = False
    try:
        result = explain_predictions("garbage", df, "text", None)
    except:
        thrown = True
    assert thrown == True, "Exception should be thrown when model does not implement predict"

