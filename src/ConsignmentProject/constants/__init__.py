from pathlib import Path
import os
from datetime import datetime
ROOT = os.getcwd()

TIMESTAMP=f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"
CONFIG_FILE_PATH = Path("configs/config.yaml")

SCHEMA_FILE_PATH = Path("configs/schema.yaml")

MODEL_FILE_PATH = Path("configs/model.yaml")

CLEANED_FILE_NAME = "cleaned_consignment_data.csv"

TRAIN_FILE_NAME = "train.npz"
TEST_FILE_NAME = "test.npz"

BEST_MODEL_KEY = "best_model"
HISTORY_KEY = "history"
MODEL_PATH_KEY = "model_path"
