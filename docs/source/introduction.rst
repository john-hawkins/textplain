Introduction
============

``Textplainer`` is a Python package and application which allows you to explain
the contributions of text data to machine learning models.
It will demonstrate the extent to which your text fields are contributing
to predictions, and the specific features of the text that are
most relevant to the prediction.

The current implementation has been developed in Python 3 and tested on a variety of
CSV files. 


Motivation
**********

Text data can add significant value to machine learning projects. There are a wide 
variety of methods of preparing text for a machine learning model. While the diversity
of approaches provides predictive utility, it does not permit simple understanding of
how the text contributes to predictions machanically.

We want to provide a simple, universal method to understand how text contributes to
a model's output. This explanation will be provided in a manner that is similar to the
way humans understand the contributions of text to meaning: through word choice, 
specificity and complexity.  


Limitations
***********

The current implementation has the following limitations:

* The quality and coverage of the synonym dictionaries. 
* Word contributions are evaluated independently.

