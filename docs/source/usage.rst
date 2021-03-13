Usage Guide
===========

Textplainer can be invoked from the command line:

.. code-block:: bash

    >textplainer


Without parameters it will print out an error and the following usage :

.. code-block:: bash

    * NOTE: Synonym dictionary is improved by installing wordnet : nltk.download('wordnet') 
    ERROR: MISSING ARGUMENTS
    USAGE 
    textplainer  [ARGS] <PATH TO SERLIALISED MODEL> <TEXT COLUMN NAME> <PATH TO TEST DATA>
     <PATH TO MODEL>   - Pickled model that adheres to the Interface.
     <COLUMN NAME>     - Name of the column that containts text data.
     <PATH TO DATA>    - Path to a dataset to explain the text value contribution.

The *NOTE* at the top will only be shown before you install the wordnet corpus. Once it is
installed it will disappear. 

The command line usage makes it clear that using textplainer requires three key pieces of
data. We need the model to be explained, which must adhere to the simple interface defined
in the file in the file :doc:`Model Interface <model-interface>` 

The list of columns to process and the path to the dataset are both mandatory.

The rest of the options turn on or off particular groups of features.

