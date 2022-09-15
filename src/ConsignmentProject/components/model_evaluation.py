from ConsignmentProject.entity import ModelEvaluationConfig, DataCleaningArtifact, ModelTrainerArtifact, ModelEvaluationArtifact, evaluate_regression_model
from ConsignmentProject.constants import *
from ConsignmentProject.utils import read_yaml_file,read_yaml, load_data, load_object, write_yaml_file

import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

class ModelEvaluation:
    def __init__(self, model_evaluation_config=ModelEvaluationConfig,
    data_cleaning_artifact= DataCleaningArtifact,
    model_trainer_artifact=ModelTrainerArtifact
    ):
        self.model_evaluation_config = model_evaluation_config
        self.model_trainer_artifact = model_trainer_artifact
        self.data_cleaning_artifact = data_cleaning_artifact

    def get_best_model(self):

        model = None
        model_evaluation_file_path = self.model_evaluation_config.model_evaluation_file_path

        if not os.path.exists(model_evaluation_file_path):
            write_yaml_file(file_path=model_evaluation_file_path,)
            return model
        
        model_eval_file_content = read_yaml_file(file_path=model_evaluation_file_path)

        model_eval_file_content = dict() if model_eval_file_content is None else model_eval_file_content

        if BEST_MODEL_KEY not in model_eval_file_content:
            return model

        model = load_object(file_path=model_eval_file_content[BEST_MODEL_KEY][MODEL_PATH_KEY])
        return model
    
    def update_evaluation_report(self, model_evaluation_artifact: ModelEvaluationArtifact):

        eval_file_path = self.model_evaluation_config.model_evaluation_file_path
        model_eval_content = read_yaml_file(file_path=eval_file_path)
        model_eval_content = dict() if model_eval_content is None else model_eval_content
        
        
        previous_best_model = None
        if BEST_MODEL_KEY in model_eval_content:
            previous_best_model = model_eval_content[BEST_MODEL_KEY]

        # logging.info(f"Previous eval result: {model_eval_content}")
        eval_result = {
            BEST_MODEL_KEY: {
                MODEL_PATH_KEY: model_evaluation_artifact.evaluated_model_path,
            }
        }

        if previous_best_model is not None:
            model_history = {self.model_evaluation_config.time_stamp: previous_best_model}
            if HISTORY_KEY not in model_eval_content:
                history = {HISTORY_KEY: model_history}
                eval_result.update(history)
            else:
                model_eval_content[HISTORY_KEY].update(model_history)

        model_eval_content.update(eval_result)
        # logging.info(f"Updated eval result:{model_eval_content}")
        write_yaml_file(file_path=eval_file_path, data=model_eval_content)

    def outlierhandler(self):
        df = pd.read_csv(self.data_cleaning_artifact.cleaned_data_file_path)

        quartile_1 = df['Unit of Measure (Per Pack)'].quantile(0.99)
        df = df[df["Unit of Measure (Per Pack)"] < quartile_1]

        quartile_2 = df['Pack Price'].quantile(0.99)
        df = df[df["Pack Price"] < quartile_2]

        quartile_3 = df['Unit Price'].quantile(0.99)
        df = df[df["Unit Price"] < quartile_3]

        quartile_5 = df['days to Process'].quantile(0.1)
        df = df[df["days to Process"] > quartile_5]

        quartile_6 = df['days to Process'].quantile(0.99)
        df = df[df["days to Process"] < quartile_6]

        return df
    def split_data_as_train_test(self):
        df = self.outlierhandler()

        df_train, df_test = train_test_split(df, train_size = 0.7, random_state = 100)

        return df_train, df_test
    
    def initiate_model_evaluation(self) -> ModelEvaluationArtifact:

        trained_model_file_path = self.model_trainer_artifact.trained_model_file_path
        trained_model_object = load_object(file_path=trained_model_file_path)

        


        # train_file_path = self.data_ingestion_artifact.train_file_path
        # test_file_path = self.data_ingestion_artifact.test_file_path

        schema_file_path = SCHEMA_FILE_PATH

        # train_dataframe = load_data(file_path=train_file_path,schema_file_path=schema_file_path,
        # )
        # test_dataframe = load_data(file_path=test_file_path,schema_file_path=schema_file_path,
        # )

        train_dataframe, test_dataframe = self.split_data_as_train_test()
        schema_content = read_yaml(path_to_yaml=schema_file_path)
        target_column_name = schema_content.target_column

        # target_column
        # logging.info(f"Converting target column into numpy array.")
        train_target_arr = np.array(train_dataframe[target_column_name])
        test_target_arr = np.array(test_dataframe[target_column_name])
        # logging.info(f"Conversion completed target column into numpy array.")

        # dropping target column from the dataframe
        # logging.info(f"Dropping target column from the dataframe.")
        train_dataframe.drop(target_column_name, axis=1, inplace=True)
        test_dataframe.drop(target_column_name, axis=1, inplace=True)
        # logging.info(f"Dropping target column from the dataframe completed.")

        model = self.get_best_model()

        if model is None:
            # logging.info("Not found any existing model. Hence accepting trained model")
            model_evaluation_artifact = ModelEvaluationArtifact(evaluated_model_path=trained_model_file_path,
            is_model_accepted=True
            )
            self.update_evaluation_report(model_evaluation_artifact)
            # logging.info(f"Model accepted. Model eval artifact {model_evaluation_artifact} created")

            return model_evaluation_artifact

        model_list = [model, trained_model_object]

        metric_info_artifact = evaluate_regression_model(model_list=model_list,
        X_train=train_dataframe,
        y_train=train_target_arr,
        X_test=test_dataframe,
        y_test=test_target_arr,
        base_accuracy=self.model_trainer_artifact.model_accuracy,
        )
        # logging.info(f"Model evaluation completed. model metric artifact: {metric_info_artifact}")

        if metric_info_artifact is None:
            response = ModelEvaluationArtifact(is_model_accepted=False,
            evaluated_model_path=trained_model_file_path
            )
            # logging.info(response)
            return response

        if metric_info_artifact.index_number == 1:
            model_evaluation_artifact = ModelEvaluationArtifact(evaluated_model_path=trained_model_file_path,
            is_model_accepted=True)
            self.update_evaluation_report(model_evaluation_artifact)
            # logging.info(f"Model accepted. Model eval artifact {model_evaluation_artifact} created")

        else:
            # logging.info("Trained model is no better than existing model hence not accepting trained model")
            model_evaluation_artifact = ModelEvaluationArtifact(evaluated_model_path=trained_model_file_path,
            is_model_accepted=False
            )

        return model_evaluation_artifact