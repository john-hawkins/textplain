import pandas as pd
import numpy as np
from textplainer.explain import explain_prediction
from textplainer.explain import explain_predictions
from textplainer.ModelInterface import ModelInterface

def test_result_length():
    null_model = ModelInterface("NULL")
    df = pd.DataFrame({"id":[1,2],"text":["the cat","the hat"]})
    result = explain_predictions(null_model, df, "text", None)
    assert len(result) == len(df), "Explain function returns results for all records"


def test_result_attributes():
    null_model = ModelInterface("NULL")
    df = pd.DataFrame({"id":[1,2],"text":["the cat","the hat"]})
    result = explain_predictions(null_model, df, "text", None)
    assert str(type(result)) == "<class 'list'>", "Explain function returns a list"
    assert str(type(result[0])) == "<class 'str'>", "Returned list contains strings"

