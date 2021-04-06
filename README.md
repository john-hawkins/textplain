textplainer
----------
> :warning: **Non-Functional**: This project is under development.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![build](https://github.com/john-hawkins/textplainer/workflows/Build/badge.svg)


This is an application to analyse the contribution of a text column to the performance
of a machine learning model. The text data could be the only feature, or one column among
many others. The application will provide local feature impact analysis to understand
the specific qualities of the text (at word level) that are pushing model 
predictions either up or down.

### Distribution

To be released and distributed via setuptools/PyPI/pip for Python 3.


### Resources & Dependencies

For Part of Speech Tagging we use [spacy](https://spacy.io/usage/spacy-101)
Note: After install you will need to get spaCy to download the English model.
```
sudo python3 -m spacy download en
```

We have built an internal synonym antonym dictionary from public access material.
For an extended dictionary of synonyms and antonyms we use wordnet from NLTK
You will need to install wordnet post-package-install.
```
import nltk
nltk.download('wordnet')
```


## Usage

To use the application you will need a model that adheres to a 
[simple interface](textplainer/ModelInterface.py)
It should go without saying that the model will need to utilise at
least one text column. The model artefact should also contain
any preprocessing required on the text. 
You will need a raw dataset containing text that you
want to explain how it contributes to the model output.


You can use this application multiple ways

Use the runner without installing the application. 

```
./textplainer-runner.py mymodel.pkl question data/test.csv > output.txt
```

Alternatively, you can invoke the directory as a package:
 
```
python -m textplainer 
```

Or simply install the package and use the command line application directly


# Installation
Installation from the source tree:

```
python setup.py install
```

(or via pip from PyPI):

```
pip install textplainer
```

Now, the ``textplainer`` command is available::

```
textplainer mymodel.pkl question data/test.csv > output.txt
```


