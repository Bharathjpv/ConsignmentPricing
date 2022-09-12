from ConsignmentProject.constants import *
from ConsignmentProject.entity import DataIngestionConfig, DataPreTransformationConfig, TrainingPipelineConfig
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
    
    def get_data_pretranformation_config(self) ->DataPreTransformationConfig:
        config = self.config.data_pre_transformation_config

        artifact_dir = self.training_pipeline_config.artifact_dir

        pre_transformed_file_dir = os.path.join(artifact_dir,config.pre_transformed_file_dir)

        pre_transformed_file_dir
        
        data_pretransforamtion_config= DataPreTransformationConfig(
            pre_transformed_file_dir=pre_transformed_file_dir
        )

        return data_pretransforamtion_config

    def get_training_pipeline_config(self) -> TrainingPipelineConfig:
        config = self.config.training_pipeline_config
        artifact_dir = os.path.join(ROOT, config.artifact_dir)

        training_pipeline_config = TrainingPipelineConfig(
            artifact_dir = artifact_dir
        )

        return training_pipeline_config