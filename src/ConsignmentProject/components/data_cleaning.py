from ConsignmentProject.entity import DataIngestionArtifact, DataCleaningArtifact
from ConsignmentProject.entity import DataCleaningConfig
from ConsignmentProject.constants import *

import pandas as pd
import numpy as np
import os

class DataCleaning:
    def __init__(self, data_ingestion_artifact:DataIngestionArtifact, data_cleaning_config: DataCleaningConfig):

        self.data_ingestion_artifact = data_ingestion_artifact
        self.data_cleaning_config = data_cleaning_config

    def transformData(self) -> DataCleaningArtifact:
        
        df = pd.read_csv(self.data_ingestion_artifact.data_file_path)

        df = df.drop('Dosage',axis = 1)
        df = df.drop(['ID', 'Project Code'], axis= 1)
        df = df.drop('Managed By', axis=1)
        df = df.drop('Vendor', axis=1)
        df = df.drop('Item Description', axis= 1)
        df = df.drop('Molecule/Test Type',axis=1)
        df = df.drop('Brand', axis= 1)
        df = df.drop('Dosage Form', axis= 1)
        df = df.drop('Weight (Kilograms)', axis= 1)
        

        def two_level(x):
            if x == 'Pre-PQ Process':
                return 'Pre-PQ Process'
            else:
                return 'Post-PQ Process'

        df['PQ #'] = df['PQ #'].apply(two_level)

        # Applying function
        def red_order(x):
            x_split = x.split("-")
            x_return = x_split[0]
            return x_return

        df['PO / SO #'] = df['PO / SO #'].apply(red_order)
        df['ASN/DN #'] = df['ASN/DN #'].apply(red_order)

        other_country = df['Country'].value_counts().to_dict()
        other_cat = []
        for k,v in other_country.items():
            if v < 30:
                other_cat.append(k)

        df['Country'] = df['Country'].replace(other_cat, 'other')
        df['Vendor INCO Term'] = df['Vendor INCO Term'].replace(['DDU', 'DAP', 'CIF'], 'Other')

        def client_date(x):
            if x == 'Pre-PQ Process':
                return pd.to_datetime('01/06/2009', format="%d/%m/%Y")
            elif x == 'Date Not Captured':
                return 'Date Not Captured'
            else:
                if len(x) < 9:
                    x= pd.to_datetime(x, format="%m/%d/%y")
                    return x
                else:
                    x = x.replace('-', '/')
                    x= pd.to_datetime(x, format="%d/%m/%Y")
                    return x

        df['PQ First Sent to Client Date'] = df['PQ First Sent to Client Date'].apply(client_date)

        df.drop(df.index[df['PQ First Sent to Client Date'] == 'Date Not Captured'], inplace = True)

        def Scheduled_date(x):
            x = x.replace('-', '/')
            x = pd.to_datetime(x, format="%d/%b/%y")
            return x

        df['Scheduled Delivery Date'] = df['Scheduled Delivery Date'].apply(Scheduled_date)
        df['Delivered to Client Date'] = df['Delivered to Client Date'].apply(Scheduled_date)
        df['Delivery Recorded Date'] = df['Delivery Recorded Date'].apply(Scheduled_date)

        df['Sub Classification'] = df['Sub Classification'].replace('HIV test - Ancillary', 'HIV test')

        other_manuf = df['Manufacturing Site'].value_counts().to_dict()
        other_cat = []
        for k,v in other_manuf.items():
            if v < 50:
                other_cat.append(k)

        df['Manufacturing Site'] = df['Manufacturing Site'].replace(other_cat, 'other')

        def other_cate(x):
            if x.find('See') != -1:
                return np.nan
            elif x == 'Freight Included in Commodity Cost' or x == 'Invoiced Separately':
                return 0
            else:
                return x

        df['Freight Cost (USD)'] = df['Freight Cost (USD)'].apply(other_cate)

        df.rename(columns=
            {
            'PQ #': "PQ",
            'PO / SO #': "PO / SO",
            'ASN/DN #': "ASN/DN"
            },
            inplace = True
        )
        df['days to Process'] = df['Delivery Recorded Date'] - df['PQ First Sent to Client Date']

        def to_int(x):
            x = np.timedelta64(x, 'ns')
            days = x.astype('timedelta64[D]')
            x = days / np.timedelta64(1, 'D')
            return x

        df['days to Process'] = df['days to Process'].apply(to_int)

        df = df.drop(['PQ First Sent to Client Date',
       'PO Sent to Vendor Date', 'Scheduled Delivery Date',
       'Delivered to Client Date', 'Delivery Recorded Date', 'Product Group'], axis=1)

        return df


    def save_cleaned_data(self):
        data = self.transformData()

        cleaned_file_path = self.data_cleaning_config.cleaned_file_dir

        cleaned_data_path = os.path.join(cleaned_file_path, CLEANED_FILE_NAME)

        os.makedirs(cleaned_file_path, exist_ok=True)

        data.to_csv(cleaned_data_path, index=None, header=True)

        return cleaned_data_path

    def initiate_data_cleaning(self):

        data_cleaning_artifact = DataCleaningArtifact(
            cleaned_data_file_path=self.save_cleaned_data()
        )

        return data_cleaning_artifact

        

