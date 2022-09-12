from ConsignmentProject.entity import DataValidationConfig, DataValidationArtifact, DataPreTransformationArtifact
from ConsignmentProject.utils import read_yaml


import pandas as pd
import collections

class DataValidation:

    def __init__(self, data_validation_config: DataValidationConfig, data_pre_transformation_artifact: DataPreTransformationArtifact):

        self.data_validation_config = data_validation_config
        self.data_pre_transformation_artifact = data_pre_transformation_artifact

    def get_df(self):
        df = pd.read_csv(self.data_pre_transformation_artifact.pre_transformed_data_file_path)

        return df

    def is_df_file_exists(self) -> bool:
        
        is_data_exists = False

        data_file_path = self.data_pre_transformation_artifact.pre_transformed_data_file_path

        is_available = os.path.exists(data_file_path)

        if not is_available:
            data_file_path = self.data_pre_transformation_artifact.pre_transformed_data_file_path

            message = "data file is not present"
        return is_available
    
    def validate_dataset_schema(self) -> bool:
        validation_sataus = False
        df = self.get_df()

        schema_path = self.data_validation_config.schema_file_path
        schema_info = read_yaml(schema_path)

        columns = schema_info.columns.keys()
        
        if len(df.columns) == len(columns):
            if collections.Counter(list(columns)) == collections.Counter(df.columns):
                validation_sataus = True

        return validation_sataus

    def initiate_data_validation(self):

        schema_file_path = self.data_validation_config.schema_file_path

        data_vaidation_artifact=DataValidationArtifact(schema_file_path=schema_file_path,
        is_validated = self.validate_dataset_schema(),
        message= "validated"
        )

        return data_vaidation_artifact


