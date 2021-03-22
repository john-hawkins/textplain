import pickle

def load_model(path_to_model):
    """
    Load and un-pickle a ML model. Model will need to implement the interface.

    :returns: A model object that implements the ModelInterface
    :rtye:  
    """
    return pickle.load(open(path_to_model, 'rb'))

def score_dataset(model, data):
    """
    Apply a model to the given dataset.

    :returns: A numpy array of model score same length as the dataset
    :rtye: numpy array
    """
    return model.predict(data)

