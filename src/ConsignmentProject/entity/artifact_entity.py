from collections import namedtuple

DataIngestionArtifact = namedtuple("DataIngestionArtifact", ["data_file_path"])

DataPreTransformationArtifact = namedtuple("DataPreTransformationArtifact", ['pre_transformed_data_file_path'])

DataValidationArtifact = namedtuple("DataValidationArtifact",
["schema_file_path","is_validated","message"])