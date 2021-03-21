import pandas as pd
import numpy as np
from textplainer.explain import explain_prediction
from textplainer.explain import explain_predictions
from textplainer.Textplain import Textplain
from textplainer.ModelInterface import ModelInterface
from textplainer.dictionary import get_synonyms_and_antonyms
from textplainer.dictionary import get_fallows_synonyms_and_antonyms
from .TestModels import SingleWordModel
from .TestModels import MultiWordModel

########################################################################################
def test_Textplain_constructor():
    texty = Textplain("My sample sentence. There are two parts.", 1, 0)
    assert texty.baseline == 1.0,  "Member variable populated"
    assert texty.impact == 1.0, "Impact calculated "
    assert len(texty.sentences) == 2, "Right number of sentences extracted"


########################################################################################
def test_result_length():
    null_model = ModelInterface("NULL")
    df = pd.DataFrame({"id":[1,2,3],"text":["the cat","the hat","the mat"]})
    result = explain_predictions(null_model, df, "text", None)
    assert len(result) == len(df), "Explain function returns results for all records"

########################################################################################
def test_single_word_model():
    jellybean_model = SingleWordModel("JellyBeanModel", "TEXT", "jellybean")
    df = pd.DataFrame({"ID":[1,2],"TEXT":["bob eats jellybeans","jane likes to swim"]})
    result = explain_predictions(jellybean_model, df, "TEXT", None)
    assert len(result) == len(df), "Explain function returns results for all records"
    assert result[0][0] == 1, "First record contains discriminative word that perfectly explains output."
    assert result[1][0] == 0, "Second record cannot be determined"

########################################################################################
def test_multi_word_model():
    mood_model = MultiWordModel("MoodsModel", "TEXT", ["happy", "sad"])
    df = pd.DataFrame({
        "ID":[1,2],
         "TEXT":["bob is very happy today","jane is happy most mornings, but sometimes sad after school"]
    })
    result = explain_predictions(mood_model, df, "TEXT", None)
    assert len(result) == len(df), "Explain function returns results for all records"
    record_one = result[0]
    record_one_text = result[0][1]
    assert record_one_text.__contains__("happy{{0.5}}"), "happy contribution"
    record_two = result[1]
    record_two_text = result[1][1]
    assert record_two_text.__contains__("{{0.5}}"), "Words with partial contribution."
    assert record_two_text.__contains__("sad{{0.5}}"), "sad has half contribution"


########################################################################################
def test_multiple_sentences_model():
    jellybean_model = SingleWordModel("JellyBeanModel", "TEXT", "jellybean")
    df = pd.DataFrame({"ID":[1,2],"TEXT":["I eat a jellybean. Bob eats a fig.","Jane likes to swim"]})
    result = explain_predictions(jellybean_model, df, "TEXT", None)
    assert len(result) == len(df), "Explain function returns results for all records"
    assert result[0][0] == 1, "First record contains word that perfectly explains output."
    assert result[1][0] == 0, "Second record cannot be determined"
    record_one = result[0]
    print("record one:", record_one)
    record_one_text = result[0][1]
    print("record one text:", record_one_text)
    assert record_one_text.__contains__("{{1.0}}"), "One sentence with full contribution"
    assert record_one_text.__contains__("jellybean{{1.0}}"), "jellybean has full contribution"

########################################################################################
def test_dictionary():
    syns, ants = get_synonyms_and_antonyms("test")
    assert str(type(syns)) == "<class 'list'>", "Synonyms should be returned as a list"
    assert str(type(ants)) == "<class 'list'>", "Antonyms should be returned as a list"


########################################################################################
def test_fallows_dictionary():
    word = "test"
    syns, ants = get_fallows_synonyms_and_antonyms(word)
    assert str(type(syns)) == "<class 'list'>", "Synonyms should be returned as a list"
    assert str(type(ants)) == "<class 'list'>", "Antonyms should be returned as a list"
    assert len(syns) == 10, "Test string should have 10 synonyms"
    assert len(ants) == 3, "Test string should have 3 antonyms"

########################################################################################
def test_result_attributes():
    null_model = ModelInterface("NULL")
    df = pd.DataFrame({"id":[1,2],"text":["the cat","the hat"]})
    result = explain_predictions(null_model, df, "text", None)
    assert str(type(result)) == "<class 'list'>", "Explain function returns a list"
    assert str(type(result[0])) == "<class 'tuple'>", "Returned list contains tuples"
    #assert str(type(result[0][0])) == "<class 'float'>", "First element is a number"
    assert isinstance(result[0][0], float) == True, "First element is a number"
    assert str(type(result[0][1])) == "<class 'str'>", "Second element is a string"


########################################################################################
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

