from collections import namedtuple

DataIngestionArtifact = namedtuple("DataIngestionArtifact", ["data_file_path"])

DataCleaningArtifact = namedtuple("DataCleaningArtifact", ['cleaned_data_file_path'])

DataValidationArtifact = namedtuple("DataValidationArtifact",
["schema_file_path","is_validated","message"])

DataTransforamtionArtifact = namedtuple("DataTransforamtionArtifact", ["is_transformed", "message", "transformed_train_file_path", "transformed_test_file_path", "preporcessed_object_file_path"])

ModelTrainerArtifact = namedtuple("ModelTrainerArtifact", ["is_trained", "message", "trained_model_file_path","train_rmse", "test_rmse", "train_accuracy", "test_accuracy","model_accuracy"])