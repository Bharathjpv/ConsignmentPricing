from ConsignmentProject.constants import *
from ConsignmentProject.entity import DataIngestionConfig, DataCleaningConfig, DataValidationConfig, TrainingPipelineConfig
from ConsignmentProject.utils import read_yaml, create_directories
from ConsignmentProject import logger
import os

class ConfigurationManager:
    def __init__(
        self, 
        config_filepath=CONFIG_FILE_PATH):

        self.config = read_yaml(path_to_yaml=config_filepath)
        self.training_pipeline_config = self.get_training_pipeline_config()

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion_config

        artifact_dir = self.training_pipeline_config.artifact_dir
        
        raw_data_dir = os.path.join(artifact_dir, config.raw_data_dir)

        
        data_ingestion_config = DataIngestionConfig(
            dataset_download_url=config.dataset_download_url,
            raw_data_dir=raw_data_dir
        )
        return data_ingestion_config
    
    def get_data_cleaning_config(self) ->DataCleaningConfig:
        config = self.config.data_cleaning_config

        artifact_dir = self.training_pipeline_config.artifact_dir

        cleaned_file_dir = os.path.join(artifact_dir,config.cleaned_file_dir)
        
        data_cleaning_config= DataCleaningConfig(
            cleaned_file_dir=cleaned_file_dir
        )

        return data_cleaning_config
    
    def get_data_validation_config(self) -> DataValidationConfig:
        config = self.config.data_validation_config
        artifact_dir = self.training_pipeline_config.artifact_dir

        data_validation_artifact_dir = os.path.join(
            artifact_dir,
            config.schema_dir
        )

        schema_file_path = SCHEMA_FILE_PATH

        data_validation_config = DataValidationConfig(
            schema_file_path= schema_file_path
        )

        return data_validation_config

    def get_training_pipeline_config(self) -> TrainingPipelineConfig:
        config = self.config.training_pipeline_config
        artifact_dir = os.path.join(ROOT, config.artifact_dir)

        training_pipeline_config = TrainingPipelineConfig(
            artifact_dir = artifact_dir
        )

        return training_pipeline_config