from collections import namedtuple

DataIngestionArtifact = namedtuple("DataIngestionArtifact", ["data_file_path"])

DataCleaningArtifact = namedtuple("DataCleaningArtifact", ['cleaned_data_file_path'])

DataValidationArtifact = namedtuple("DataValidationArtifact",
["schema_file_path","is_validated","message"])

DataTransforamtionArtifact = namedtuple("DataTransforamtionArtifact", ["is_transformed", "message", "transformed_train_file_path", "transformed_test_file_path", "preporcessed_object_file_path"])

