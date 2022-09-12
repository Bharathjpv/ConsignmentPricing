from collections import namedtuple


DataIngestionConfig = namedtuple("DataIngestion", [
    "dataset_download_url",
    "raw_data_dir"
])

DataPreTransformationConfig = namedtuple("DataPreTransformation", ["pre_transformed_file_dir"])

DataValidationConfig = namedtuple("DataValidation", ["schema_file_path"])


TrainingPipelineConfig = namedtuple("TrainingPipeline", ["artifact_dir"])