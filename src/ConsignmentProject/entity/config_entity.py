from collections import namedtuple


DataIngestionConfig = namedtuple("DataIngestion", [
    "dataset_download_url",
    "raw_data_dir"
])

DataCleaningConfig = namedtuple("DataCleaningConfig", ["cleaned_file_dir"])

DataValidationConfig = namedtuple("DataValidation", ["schema_file_path"])

DataTransforamtionConfig = namedtuple("DataTransformation", ["transformed_train_dir", "transformed_test_dir", "preprocessed_object_file_path"])

ModelTrainerConfig = namedtuple("ModelTrainerConfig", ["model_file_name", "trained_model_file_path","base_accuracy", "model_config_file_path"])

ModelEvaluationConfig = namedtuple("ModelEvaluationConfig", ["model_evaluation_file_path"])

ModelPusherConfig = namedtuple("ModelPusherConfig", ["export_dir_path"])

TrainingPipelineConfig = namedtuple("TrainingPipeline", ["artifact_dir"])