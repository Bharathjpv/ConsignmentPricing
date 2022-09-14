import numpy as np
import pandas as pd
import dill
import os
import yaml

def write_yaml_file(file_path:str,data:dict=None):
    """
    Create yaml file 
    file_path: str
    data: dict
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path,"w") as yaml_file:
        if data is not None:
            yaml.dump(data,yaml_file)

def read_yaml_file(file_path:str)->dict:
    """
    Reads a YAML file and returns the contents as a dictionary.
    file_path: str
    """
    with open(file_path, 'rb') as yaml_file:
        return yaml.safe_load(yaml_file)



def save_numpy_array_data(file_path: str, array: np.array):
    """
    Save numpy array data to file
    file_path: str location of file to save
    array: np.array data to save
    """

    dir_path = os.path.dirname(file_path)
    os.makedirs(dir_path, exist_ok=True)
    with open(file_path, 'wb') as file_obj:
        np.save(file_obj, array)

def load_numpy_array_data(file_path: str) -> np.array:
    """
    load numpy array data from file
    file_path: str location of file to load
    return: np.array data loaded
    """

    with open(file_path, 'rb') as file_obj:
        return np.load(file_obj)

def save_object(file_path:str,obj):
    """
    file_path: str
    obj: Any sort of object
    """
    if os.path.exists(file_path):
        os.remove(file_path)
    dir_path = os.path.dirname(file_path)
    os.makedirs(dir_path, exist_ok=True)
    with open(file_path, "wb") as file_obj:
        dill.dump(obj, file_obj)

def load_object(file_path:str):
    """
    file_path: str
    """
    with open(file_path, "rb") as file_obj:
        return dill.load(file_obj)


def load_data(file_path: str, schema_file_path: str) -> pd.DataFrame:
    datatset_schema = read_yaml_file(schema_file_path)

    schema = datatset_schema[DATASET_SCHEMA_COLUMNS_KEY]

    dataframe = pd.read_csv(file_path)

    error_messgae = ""


    for column in dataframe.columns:
        if column in list(schema.keys()):
            dataframe[column].astype(schema[column])
        else:
            error_messgae = f"{error_messgae} \nColumn: [{column}] is not in the schema."
    if len(error_messgae) > 0:
        raise Exception(error_messgae)
    return dataframe

