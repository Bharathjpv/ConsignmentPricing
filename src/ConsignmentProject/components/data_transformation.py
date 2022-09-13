from ConsignmentProject.entity import DataTransforamtionConfig, DataValidationArtifact,DataCleaningArtifact, DataTransforamtionArtifact
from ConsignmentProject.constants import *
from ConsignmentProject.utils import read_yaml, save_numpy_array_data, save_object
from ConsignmentProject.exception import ConsignmentException

import os, sys
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline


class DataTransformation:

    def __init__(self, data_transformationc_config:DataTransforamtionConfig,
    data_validation_artifact:DataValidationArtifact,
    data_cleaning_artifact:DataCleaningArtifact):

        self.data_transformationc_config = data_transformationc_config
        self.data_validation_artifact = data_validation_artifact
        self.data_cleaning_artifact = data_cleaning_artifact

    def outlierhandler(self):
        df = pd.read_csv(self.data_cleaning_artifact.cleaned_data_file_path)

        quartile_1 = df['Unit of Measure (Per Pack)'].quantile(0.99)
        df = df[df["Unit of Measure (Per Pack)"] < quartile_1]

        quartile_2 = df['Pack Price'].quantile(0.99)
        df = df[df["Pack Price"] < quartile_2]

        quartile_3 = df['Unit Price'].quantile(0.99)
        df = df[df["Unit Price"] < quartile_3]

        quartile_5 = df['days to Process'].quantile(0.1)
        df = df[df["days to Process"] > quartile_5]

        quartile_6 = df['days to Process'].quantile(0.99)
        df = df[df["days to Process"] < quartile_6]

        return df
    
    def split_data_as_train_test(self):
        df = self.outlierhandler()

        df_train, df_test = train_test_split(df, train_size = 0.7, random_state = 100)

        return df_train, df_test
    
    def get_data_transformer_object(self) -> ColumnTransformer:

        schema_file_path = self.data_validation_artifact.schema_file_path

        dataset_schema = read_yaml(schema_file_path)

        numerical_columns = dataset_schema.numerical_columns
        categorical_columns = dataset_schema.categorical_columns

        num_pipeine = Pipeline(steps = [
            ('imputer', SimpleImputer(strategy="median")),
            ('scaler', StandardScaler())
        ])

        cat_pipeline = Pipeline(steps=[
            ('impute', SimpleImputer(strategy='most_frequent')),
            ('one_hot_encoder', OneHotEncoder()),
            ('scaler', StandardScaler(with_mean=False))
        ])

        preprocessing = ColumnTransformer([
            ('num_pipeine', num_pipeine, numerical_columns),
            ('cat_pipeline', cat_pipeline, categorical_columns)
        ])

        return preprocessing
    
    def initiate_data_transformation(self) -> DataTransforamtionArtifact:
        try:
            preprocessing_obj = self.get_data_transformer_object()

            train_df, test_df = self.split_data_as_train_test()

            schema = read_yaml(SCHEMA_FILE_PATH)

            target_column_name = schema.target_column

            input_feature_train_df = train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df = test_df[target_column_name]

            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)
            input_feature_train_arr=input_feature_train_arr.toarray()
            input_feature_test_arr=input_feature_test_arr.toarray()
            # print(input_feature_train_arr.shape, np.array(target_feature_train_df).shape,)

            train_arr = np.c_[ input_feature_train_arr, np.array(target_feature_train_df).reshape(-1,1)]

            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df).reshape(-1,1)]

            transformed_train_dir = self.data_transformationc_config.transformed_train_dir
            transformed_test_dir = self.data_transformationc_config.transformed_test_dir

            transformed_train_file_path = os.path.join(transformed_train_dir, TRAIN_FILE_NAME)
            transformed_test_file_path = os.path.join(transformed_test_dir, TEST_FILE_NAME)

            save_numpy_array_data(transformed_train_file_path, array= train_arr)
            save_numpy_array_data(transformed_test_file_path, array= test_arr)

            preprocessing_obj_file_path = self.data_transformationc_config.preprocessed_object_file_path

            save_object(file_path= preprocessing_obj_file_path, obj= preprocessing_obj)

            data_transformation_artifact = DataTransforamtionArtifact(
                is_transformed= True,
                message= "Data Transformation Successfull",
                transformed_train_file_path= transformed_train_file_path,
                transformed_test_file_path= transformed_test_file_path,
                preporcessed_object_file_path=preprocessing_obj_file_path
                )
            
            return data_transformation_artifact
        except Exception as e:
            raise ConsignmentException(e, sys) from e