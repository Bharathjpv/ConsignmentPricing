from ConsignmentProject.components import DataIngestion, DataValidation, DataCleaning
from ConsignmentProject.config import ConfigurationManager


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
    print(datavalidationartifact)
    

if __name__=="__main__":
    try:
        main()
    except Exception as e:
        raise e