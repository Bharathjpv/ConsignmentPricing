from ConsignmentProject.constants import *
from ConsignmentProject.entity import DataIngestionConfig, ModelTrainerConfig,DataCleaningConfig, DataValidationConfig,DataTransforamtionConfig,ModelEvaluationConfig, ModelPusherConfig, TrainingPipelineConfig
from ConsignmentProject.utils import read_yaml, create_directories
from ConsignmentProject import logger


import os

class ConfigurationManager:
    def __init__(
        self, 
        config_filepath=CONFIG_FILE_PATH,time_stamp=TIMESTAMP):

        self.config = read_yaml(path_to_yaml=config_filepath)
        self.timestamp=time_stamp
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
        
        artifact_dir = self.training_pipeline_config.artifact_dir

        
        schema_file_path = SCHEMA_FILE_PATH

        data_validation_config = DataValidationConfig(
            schema_file_path= schema_file_path
        )

        return data_validation_config
    
    def get_data_tranformation_config(self) -> DataTransforamtionConfig:
        config = self.config.data_transformation_config
        artifact_dir = self.training_pipeline_config.artifact_dir

        data_transformation_artifact_dir = os.path.join(artifact_dir, config.transformed_dir)

        transformed_train_dir = os.path.join(artifact_dir,config.transformed_dir, config.transformed_train_dir)

        transformed_test_dir = os.path.join(artifact_dir, config.transformed_dir, config.transformed_test_dir)

        preprocessed_object_file_path = os.path.join(artifact_dir, config.transformed_dir, config.preprocession_dir, config.preprocessed_object_file_name)

        data_transformation_config = DataTransforamtionConfig(
        transformed_train_dir= transformed_train_dir,
        transformed_test_dir= transformed_test_dir,
        preprocessed_object_file_path= preprocessed_object_file_path
        )

        return data_transformation_config
    
    def get_model_trainer_config(self) -> ModelTrainerConfig:
        config = self.config.model_trainer_config

        artifact_dir = self.training_pipeline_config.artifact_dir

        trained_model_file_path = os.path.join(
            artifact_dir,
            config.trained_model_dir
        )

        model_file_name = os.path.join(trained_model_file_path, config.model_file_name)
        


        model_config_file_path = MODEL_FILE_PATH

        base_accuracy = config.base_accuracy

        model_trainer_config=ModelTrainerConfig(
            trained_model_file_path= model_file_name,
            model_file_name= model_file_name,
            base_accuracy= base_accuracy,
            model_config_file_path = model_config_file_path
        )

        return model_trainer_config
    
    def get_model_evaluation_config(self) -> ModelEvaluationConfig:

        config = self.config.model_evaluation_config

        artifact_dir = self.training_pipeline_config.artifact_dir

        model_evaluation_dir = os.path.join(artifact_dir, config.model_evaluation_dir)

        model_evaluation_file_path = os.path.join(model_evaluation_dir, config.model_evaluation_file_name)

        model_evaluation_config = ModelEvaluationConfig(model_evaluation_file_path= model_evaluation_file_path
        )

        return model_evaluation_config
    
    def get_model_pusher_config(self) -> ModelPusherConfig:

        # time_stamp = f"{datetime.now().strftime('%Y%m%d%H%M%S')}"
        model_pusher_config_info = self.config.model_pusher_config
        export_dir_path = os.path.join(ROOT, model_pusher_config_info.model_export_dir,self.timestamp)

        model_pusher_config = ModelPusherConfig(export_dir_path=export_dir_path)
        # logging.info(f"Model pusher config {model_pusher_config}")
        return model_pusher_config

    def get_training_pipeline_config(self) -> TrainingPipelineConfig:
        config = self.config.training_pipeline_config
        artifact_dir = os.path.join(ROOT, config.artifact_dir,self.timestamp)

        training_pipeline_config = TrainingPipelineConfig(
            artifact_dir = artifact_dir
        )

        return training_pipeline_config