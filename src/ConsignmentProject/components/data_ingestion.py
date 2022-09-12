import pandas as pd
from six.moves import urllib

import os
from ConsignmentProject.entity import DataIngestionConfig, DataIngestionArtifact


class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def download_consignment_data(self) -> DataIngestionArtifact:

        # url of dataset
        dataset_download_url = self.config.dataset_download_url

        raw_data_dir = self.config.raw_data_dir

        os.makedirs(raw_data_dir,exist_ok=True)

        consignment_file_name = os.path.basename(dataset_download_url)

        data_file_path = os.path.join(raw_data_dir, consignment_file_name)

        urllib.request.urlretrieve(dataset_download_url, data_file_path)

        data_ingestion_artifact = DataIngestionArtifact(
            data_file_path = data_file_path
        )
        return data_file_path
    
    def DataArtifact(self) -> DataIngestionArtifact:

        data_file_path = self.download_consignment_data()

        data_ingestion_artifact= DataIngestionArtifact(
            data_file_path=data_file_path
        )

        return data_ingestion_artifact
    
    def initiate_data_ingestion(self):
        return self.DataArtifact()