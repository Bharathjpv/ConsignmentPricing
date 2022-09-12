from ConsignmentProject.components import DataIngestion, DataPreTransformation
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
    

if __name__=="__main__":
    try:
        main()
    except Exception as e:
        raise e