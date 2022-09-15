import os
import sys

from ConsignmentProject.exception import ConsignmentException

import pandas as pd


class ConsignmentData:

    def __init__(self,
                PQ: str,
                PO: str,
                DN: str,
                Country: str,
                Fulfill: str,
                Vendor: str,
                Shipment: str,
                Classification: str,
                Manufacturing: str,
                Designation: str,
                PerPack: int,
                LineItemQuantity: int,
                PackPrice: float,
                UnitPrice: float,
                FreightCost: float,
                LineItemInsurance: float,
                daystoProcess: float,
                LineItemValue: float = None
                ):
        try:
            self.PQ = PQ,
            self.PO = PO,
            self.DN = DN,
            self.Country=Country,
            self.Fulfill=Fulfill,
            self.Vendor=Vendor,
            self.Shipment=Shipment,
            self.Classification=Classification,
            self.Manufacturing=Manufacturing,
            self.Designation=Designation,
            self.PerPack=PerPack,
            self.LineItemQuantity=LineItemQuantity,
            self.PackPrice =PackPrice,
            self.UnitPrice =UnitPrice,
            self.FreightCost =FreightCost,
            self.LineItemInsurance=LineItemInsurance ,
            self.daystoProcess =daystoProcess,
            self.LineItemValue=LineItemValue
        except Exception as e:
            raise ConsignmentException(e, sys) from e

    def get_housing_input_data_frame(self):

        try:
            consignment_input_dict = self.get_housing_data_as_dict()
            return pd.DataFrame(housing_input_dict)
        except Exception as e:
            raise ConsignmentException(e, sys) from e

    def get_housing_data_as_dict(self):
        try:
            input_data = {
                "PQ": [self.PQ],
                "PO / SO":[self.PO],
                "ASN/DN": [self.DN],
                "Country": [self.Country],
                "Fulfill Via": [self.Fulfill],
                "Vendor INCO Term": [self.Vendor],
                "Shipment Mode": [self.Shipment],
                "Sub Classification": [self.Classification],
                "Manufacturing Site": [self.Manufacturing],
                "First Line Designation": [self.Designation],
                "Unit of Measure (Per Pack)": [self.PerPack],
                "Line Item Quantity": [self.LineItemQuantity],
                "Pack Price": [self.PackPrice],
                "Unit Price": [self.UnitPrice],
                "Freight Cost (USD)": [self.FreightCost],
                "Line Item Insurance (USD)": [self.LineItemInsurance],
                "days to Process": [self.daystoProcess]
                }
            return input_data
        except Exception as e:
            raise ConsignmentException(e, sys)


class ConsignmentPredictor:

    def __init__(self, model_dir: str):
        try:
            self.model_dir = model_dir
        except Exception as e:
            raise ConsignmentException(e, sys) from e

    def get_latest_model_path(self):
        try:
            folder_name = list(map(int, os.listdir(self.model_dir)))
            latest_model_dir = os.path.join(self.model_dir, f"{max(folder_name)}")
            file_name = os.listdir(latest_model_dir)[0]
            latest_model_path = os.path.join(latest_model_dir, file_name)
            return latest_model_path
        except Exception as e:
            raise ConsignmentException(e, sys) from e

    def predict(self, X):
        try:
            model_path = self.get_latest_model_path()
            model = load_object(file_path=model_path)
            median_house_value = model.predict(X)
            return median_house_value
        except Exception as e:
            raise ConsignmentException(e, sys) from e