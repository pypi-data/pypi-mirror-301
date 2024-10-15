import pandas as pd
import numpy as np
from catboost import CatBoostClassifier

def manipulate_testdata(xtrain: pd.DataFrame, xtest: pd.DataFrame, model: CatBoostClassifier, variable: str):
    """
    Manipulate the given variable column in test data based on values of that variable in train data.

    Parameters
    ----------
    xtrain : pd.DataFrame
            A dataframe including train data.
    xtest : pd.DataFrame
            A dataframe including test data.
    model : CatBoostClassifier
            A trained CatBoostClassifier.
    variable: str 
            Name of variable.

    Returns
    -------
    pd.DataFrame
            The manipulated data.
    """
    # create xtest_rm
    xtest_rm = xtest.copy()
    cat_indices = model.get_cat_feature_indices()
    # replace variable with mode or mean based on its type
    if xtrain.columns.get_loc(variable) not in cat_indices:
        mean_value = xtrain[variable].mean()
        xtest_rm[variable] = mean_value
    else:
        mode_value = xtrain[variable].mode()[0]
        xtest_rm[variable] = mode_value
    return xtest_rm

def convert_to_dataframe(*args):
    """
    Convert inputs to DataFrames.

    Parameters
    ----------
    Args:  *args
            A variable number of input objects that can be converted into Pandas DataFrames (e.g., lists, dictionaries, numpy arrays).

    Returns:  
    list of pd.DataFrame
            A list of Pandas DataFrames created from the input objects.    
    """
    return [pd.DataFrame(arg).reset_index(drop=True) for arg in args]

def validate_variables(variables: list, xtrain: pd.DataFrame):
    """
    Check if variables are valid and exist in the train dataset.

    Parameters
    ----------
    variables: list 
            List of variables.
    xtrain : pd.DataFrame
            A dataframe including train data.

    Raises
    -------
    ValueError
            If variables is not a list or if any variable does not exist in xtrain.
    """
    if not isinstance(variables, list):
        raise ValueError("Variables input must be a list")
    for var in variables:
        if var not in xtrain.columns:
            raise ValueError(f"{var} is not in the variables")

def check_nan(*dataframes):
    """
    Check if any of the provided DataFrames contain missing values.

    Parameters
    ----------
    *dataframes : pd.DataFrame
        A variable number of DataFrame objects to check for NaN values.

    Raises
    ------
    ValueError
        If any DataFrame contains missing (NaN) values.
    TypeError
        If any input is not a Pandas DataFrame.
    """

    for i, df in enumerate(dataframes, start=1):
        if df.isna().sum().sum() > 0:
            raise ValueError(f"DataFrame {i} contains missing values.")
