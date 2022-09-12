from collections import namedtuple


DataIngestionConfig = namedtuple("DataIngestion", [
    "dataset_download_url",
    "raw_data_dir"
])

DataPreTransformationConfig = namedtuple("DataPreTransformation", ["pre_transformed_file_dir"])

TrainingPipelineConfig = namedtuple("TrainingPipeline", ["artifact_dir"])