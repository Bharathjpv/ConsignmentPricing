from collections import namedtuple


DataIngestionConfig = namedtuple("DataIngestion", [
    "dataset_download_url",
    "raw_data_dir"
])

DataCleaningConfig = namedtuple("DataCleaningConfig", ["cleaned_file_dir"])

DataValidationConfig = namedtuple("DataValidation", ["schema_file_path"])


TrainingPipelineConfig = namedtuple("TrainingPipeline", ["artifact_dir"])