Model Interface
===============

To use Textplainer your model must implement a ```predict``` 
function that accepts a pandas DataFrame and returns 
a numpy array of floats variables.


.. code-block:: python

    class Example:

        def __init__(self):

        def predict(self, x: pd.DataFrame) -> np.ndarray:
            # Process DataFrame and 
            # return one prediction per row
            # inside a numpy array


You can either incorporate this interface into you model design,
or write a minimal wrapper class for the purpose of running textplainer.

We provide a set of re-usable wrapper classes in the experiments 
directory in the source code.


Notes and Caveats
^^^^^^^^^^^^^^^^^

In the case of binary classification the value of textplainer 
will be diminished if your model does not return a real valued 
response that indicates confidence in the prediction. For methods
like SVMs, which produce classes rather than probabilities, this 
will require using one of the techniques that infers
confidence from distance to the decision boundary.

For multi-class classification models you will need to write a wrapper
class for each class you want explained. In other words create a wrapper
that converts your multi-class model into a one-vs-all binary classifier.



