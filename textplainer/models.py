import pickle
import sys

class CustomUnpickler(pickle.Unpickler):
    def add_path(self, path):
        sys.path.append(path)
    def find_class(self, module, name):
        return super().find_class(module, name)

def load_model(path_to_model, path_to_class):
    """
    Load and un-pickle a ML model. Model will need to implement the interface.

    :returns: A model object that implements the ModelInterface
    :rtye: object
    """
    unpickler = CustomUnpickler(open(path_to_model, 'rb'))
    unpickler.add_path(path_to_class)
    return unpickler.load()

def score_dataset(model, data):
    """
    Apply a model to the given dataset.

    :returns: A numpy array of model score same length as the dataset
    :rtye: numpy array
    """
    return model.predict(data)

def load_and_test_model(path_to_model, path_to_class ):
    """
    Load and un-pickle a ML model.
    Then test if it implements the required interface.
    Else throw exception.
    :returns: A model object that implements the ModelInterface
    :rtye:
    """
    model = load_model(path_to_model, path_to_class)
    funcs = dir(model)
    if 'predict' not in funcs:
        raise Exception("ERROR: Model does not implement function 'predict'")
    else:
        return model
    
