textplainer
----------

```
Status - Non-Functional: In Development
```

This is an application to analyse the contribution of a text column to the performance
of a machine learning model. The text data could be the only feature, or one column among
many others. This application will provide local feature impact analysis to understand
the specific word fetaures that are pushing model predictions up or down.

Additional feature flags unlock features that are more computationally intensive and
generally domain specific.


### Distribution

To be released and distributed via setuptools/PyPI/pip for Python 3.


### Resources & Dependencies

For Part of Speech Tagging we use [spacy](https://spacy.io/usage/spacy-101)
Note: After install you will need to get spaCy to download the English model.
```
sudo python3 -m spacy download en
```

For a dictionary of synonyms and antonyms we use wordnet from NLTK
You will need to install wordnet post-package-install.
```
import nltk
nltk.download('wordnet')
```


## Usage

To use the application you will need a model that adheres to a [simple interface](textplainer/ModelInterface.py)
It should go without saying that the model will need to utilise a text column. Note that the model in this case
should wrap around any preprocessing required on the text. You will need a raw dataset containing text that you
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


