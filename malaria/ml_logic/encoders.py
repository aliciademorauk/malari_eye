import numpy as np
from sklearn.preprocessing import OneHotEncoder


def transform_intensities(X: np.ndarray) -> np.ndarray:
    assert isinstance(X, np.ndarray)
    X = X/255 # this divides all elements of the array to be between 0,1
    return X

def one_hot_y(y: np.ndarray) -> np.ndarray:
    assert isinstance(y, np.ndarray)
    #convert y into OneHotEncoder
    ohe = OneHotEncoder(sparse_output=False,
                        handle_unknown="ignore")
    return ohe

def one_hot_cat(ohe_in) -> np.ndarray:
    return ohe_in.categories_
