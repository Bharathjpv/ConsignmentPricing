import streamlit as st
import pickle
import time
import pandas as pd
import sys
import datetime
from ConsignmentProject.logger import logging
from ConsignmentProject.exception import ConsignmentException

from ConsignmentProject.entity import Consignment_predictor, ConsignmentData
from ConsignmentProject.pipeline.pipeline import pipeline


# model = pickle.load(open('classificationmodel.pkl', 'rb'))
# countrylist = pickle.load(open('countryname.pkl', 'rb'))
# logging = logger.applevel_logger()


@st.cache(persist=True)
def main():
    st.sidebar.header("Predict consignemnt Pricing Using Machine Learning")
    st.sidebar.text("Choose the parmeters to predict")

    st.sidebar.markdown("#### PQ")
    st.sidebar.slider('cat', 1,4,step=1)
    
if __name__ == '__main__':
    main()
