from ConsignmentProject.components import DataIngestion, DataValidation, DataCleaning, DataTransformation, ModelTrainer
from ConsignmentProject.config import ConfigurationManager

import warnings
warnings.filterwarnings("ignore")



def main():
    configMain = ConfigurationManager()

    ingestion_config = configMain.get_data_ingestion_config()
    dataingestion = DataIngestion(config=ingestion_config)
    dataIngestionArtifact = dataingestion.initiate_data_ingestion()
    
    ####################################################################
    data_cleaning_config = configMain.get_data_cleaning_config()
    
    data_cleaning = DataCleaning(dataIngestionArtifact, data_cleaning_config)

    dataCleaningArtifact = data_cleaning.initiate_data_cleaning()
    ##################################################

    data_validation_config = configMain.get_data_validation_config()

    dataValidation = DataValidation(data_validation_config=data_validation_config, data_cleaned_artifact = dataCleaningArtifact)

    datavalidationartifact = dataValidation.initiate_data_validation()
    #################################################################

    data_validation_config = configMain.get_data_tranformation_config()
    data_transformation_config = configMain.get_data_tranformation_config()

    dataTransformation = DataTransformation(data_transformationc_config=data_transformation_config, data_validation_artifact=datavalidationartifact,
    data_cleaning_artifact= dataCleaningArtifact)

    dataTransformationArtifact = dataTransformation.initiate_data_transformation()

    ###################################################################################

    model_trainer_config = configMain.get_model_trainer_config()

    modelTraniner = ModelTrainer(model_trainer_config=model_trainer_config, data_transformation_artifact= dataTransformationArtifact)

    modelTrainerArtifact = modelTraniner.initaite_model_tranier()