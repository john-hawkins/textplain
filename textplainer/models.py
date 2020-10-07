import pickle

def load_model(path_to_model):
    return pickle.load(open(path_to_model, 'rb'))

def score_dataset(model, data):
    return model.predict(data)

