from typing import Union

from fastapi import FastAPI
from ConsignmentProject.pipeline.pipeline import pipeline
from pydantic import BaseModel
from ConsignmentProject.entity.Consignment_predictor import ConsignmentData, ConsignmentPredictor

from fastapi import Body
from typing import Dict, Any

import pandas as pd

app = FastAPI()

class Data(BaseModel):
    PQ: str
    PO: str
    DN: str
    Country: str
    Fulfill: str
    Vendor: str
    Shipment: str
    Classification: str
    Manufacturing: str
    Designation: str
    PerPack: float
    LineItemQuantity: float
    PackPrice: float
    UnitPrice: float
    FreightCost: float
    LineItemInsurance: float
    daystoProcess: float


@app.get("/train")
async def read_root():
    response = pipeline()
    return response._asdict()


@app.post("/predict")
async def read_item(data: Dict[Any, Any]):
    PQ = data['PQ']
    PO = data['PO']
    DN = data['DN']
    Country = data['Country']
    Fulfill=data["Fulfill"]
    Vendor=data["Vendor"]
    Shipment=data["Shipment"]
    Classification=data["Classification"]
    Manufacturing=data["Manufacturing"]
    Designation=data["Designation"]
    PerPack=data["PerPack"]
    LineItemQuantity=data["LineItemQuantity"]
    PackPrice=data["PackPrice"]
    UnitPrice=data["UnitPrice"]
    FreightCost=data["FreightCost"]
    LineItemInsurance=data["LineItemInsurance"]
    daystoProcess=data["daystoProcess"]

    dataClass = ConsignmentData(PQ, PO, DN, Country, Fulfill, Vendor, Shipment, Classification, Manufacturing, Designation, PerPack, LineItemQuantity, PackPrice, UnitPrice, FreightCost, LineItemInsurance, daystoProcess)
    df = dataClass.get_housing_input_data_frame()
    df = pd.read_csv(r'D:\Consignment\ConsignmentPricing\artifacts\2022-09-15-13-09-23\data_cleaning\cleaned_consignment_data.csv')
    df = df.iloc[:1]

    predictorClass = ConsignmentPredictor(model_dir=r"D:\Consignment\ConsignmentPricing\saved_models\2022-09-15-13-09-23")
    
    result = predictorClass.predict(df)
    print(result)
    return data