from collections import namedtuple


DataIngestionConfig = namedtuple("DataIngestion", [
    "dataset_download_url",
    "raw_data_dir"
])

DataCleaningConfig = namedtuple("DataCleaningConfig", ["cleaned_file_dir"])

DataValidationConfig = namedtuple("DataValidation", ["schema_file_path"])

DataTransforamtionConfig = namedtuple("DataTransformation", ["transformed_train_dir", "transformed_test_dir", "preprocessed_object_file_path"])


TrainingPipelineConfig = namedtuple("TrainingPipeline", ["artifact_dir"])