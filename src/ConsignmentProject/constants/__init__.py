from pathlib import Path
import os

ROOT = os.getcwd()


CONFIG_FILE_PATH = Path("configs/config.yaml")

SCHEMA_FILE_PATH = Path("configs/schema.yaml")

CLEANED_FILE_NAME = "cleaned_consignment_data.csv"

TRAIN_FILE_NAME = "train.npz"
TEST_FILE_NAME = "test.npz"