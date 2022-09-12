from ConsignmentProject.components import DataIngestion, DataPreTransformation, DataValidation
from ConsignmentProject.config import ConfigurationManager


def main():
    configMain = ConfigurationManager()

    ingestion_config = configMain.get_data_ingestion_config()
    dataingestion = DataIngestion(config=ingestion_config)
    dataIngestionArtifact = dataingestion.initiate_data_ingestion()
    
    ####################################################################
    data_pretransformation_config = configMain.get_data_pretranformation_config()
    
    dataPreTransformation = DataPreTransformation(dataIngestionArtifact, data_pretransformation_config)

    dataPreTransformationArtifact = dataPreTransformation.initiate_data_pretranformation()

    ##################################################

    data_validation_config = configMain.get_data_validation_config()

    dataValidation = DataValidation(data_validation_config=data_validation_config, data_pre_transformation_artifact = dataPreTransformationArtifact)

    datavalidationartifact = dataValidation.initiate_data_validation()
    print(datavalidationartifact)
    

if __name__=="__main__":
    try:
        main()
    except Exception as e:
        raise e