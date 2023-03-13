import numpy as np
import pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.compose import ColumnTransformer, make_column_transformer
from sklearn.preprocessing import OneHotEncoder, FunctionTransformer
from malaria.ml_logic.encoders import transform_intensities,one_hot_y
from colorama import Fore, Style


def preprocess_features(X: np.ndarray) -> np.ndarray:

    def create_sklearn_preprocessor() -> FunctionTransformer:
        """
        Scikit-learn pipeline that transforms a cleaned dataset of shape (_, 7)
        into a preprocessed one of different fixed shape (_, 65).

        Stateless operation: "fit_transform()" equals "transform()".
        """

        image_pipe = FunctionTransformer(transform_intensities)

        return image_pipe

    print(Fore.BLUE + "\nPreprocess features..." + Style.RESET_ALL)
    preprocessor = create_sklearn_preprocessor()
    X_processed = preprocessor.fit_transform(X)
    print("✅ X_processed, with shape", X_processed.shape)

    return X_processed

def preprocess_targets(y: np.ndarray) -> np.ndarray:

    def create_sklearn_preprocessor() -> FunctionTransformer:
         """
        Scikit-learn pipeline that transforms a cleaned dataset of shape (_, 7)
        into a preprocessed one of different fixed shape (_, 65).

        Stateless operation: "fit_transform()" equals "transform()".
        """
        image_pipe = FunctionTransformer(OneHotEncoder)

        return image_pipe

    y_cat = np.unique(y)
    cell_type_pipe = make_pipeline(
                                   image_pipe
                                    )


    return cell_type_pipe
