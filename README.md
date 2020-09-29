textplain
----------

```
Status - In Development
```

This is an application to analyse the contribution of a text column to the performance
of a machine learning model. The text data could be the only feature, or one column among
many others. This application will provide local feature impact analysis to understand
the specific word fetaures that are pushing model predictions up or down.

Additional feature flags unlock features that are more computationally intensive and
generally domain specific.


### Distribution

Released and distributed via setuptools/PyPI/pip for Python 3.


### Resources & Dependencies

For Part of Speech Tagging we use [spacy](https://spacy.io/usage/spacy-101)

Note: After install you will need to get spaCy to download the English model.
```
sudo python3 -m spacy download en
```

## Usage

You can use this application multiple ways

Use the runner without installing the application. 
The following example will generate all features on the test data.

```
./textplain-runner.py -columns=question,answer -pos -literacy -traits -rhetoric -profanity -emoticons -sentiment -comparison -topics=count data/test.csv > data/output.csv
```

Alternatively, you can invoke the directory as a package:
 
```
python -m textplain -columns=question,answer data/test.csv > data/output.csv
```

Or simply install the package and use the command line application directly


# Installation
Installation from the source tree:

```
python setup.py install
```

(or via pip from PyPI):

```
pip install textplain
```

Now, the ``textplain`` command is available::

```
textplain mymodel.pkl question data/test.csv > output.txt
```


