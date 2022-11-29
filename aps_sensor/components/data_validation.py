import os
from distutils import dir_util
from aps_sensor.constant.training_pipeline import SCHEMA_FILE_PATH
from aps_sensor.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from aps_sensor.entity.config_entity import DataValidationConfig
from aps_sensor.exception import SensorException
from aps_sensor.logger import logging
from aps_sensor.utils.main_utils import read_yaml, write_yaml_file
import pandas as pd
import sys
from scipy.stats import ks_2samp


class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config=data_validation_config
            self._schema_config = read_yaml(SCHEMA_FILE_PATH)
        except Exception as e:
            raise SensorException(e, sys)

    def is_numerical_column_exist(self, dataframe: pd.DataFrame)->bool:
         try:
            numerical_columns = self._schema_config['numerical_columns']
            data_frame_columns = dataframe.columnms

            num_present: bool = True
            missing_numerical_columns = []
            for numerical_column in numerical_columns:
                if numerical_column not in data_frame_columns:
                    num_present = False
                    missing_numerical_columns.append(numerical_column)
            # if not num_present:
            logging.info(f"Missing columns list {missing_numerical_columns}")

            return num_present

         except Exception as e:
            raise SensorException(e, sys)


    def validate_number_of_columns(self, dataframe: pd.DataFrame)->bool:
        try:
            number_of_columns = self._schema_config['columns']

            if len(dataframe.columns) == number_of_columns:
                return True
            return False
        except Exception as e:
            raise SensorException(e, sys)

    @staticmethod
    def read_data(filePath)-> pd.DataFrame:
        try:
            return pd.read_csv(filePath)
        except Exception as e:
            raise SensorException(e, sys)


    def get_drift_report(self, base_df,current_df,threshold=0.05):

        try:
            status = True
            report ={}
            for column in base_df.columns:
                d1 = base_df[column]
                d2  = current_df[column]
                is_same_dist = ks_2samp(d1,d2)
                if threshold<=is_same_dist.pvalue:
                    is_found=False
                else:
                    is_found = True 
                    status=False
                report.update({column:{
                    "p_value":float(is_same_dist.pvalue),
                    "drift_status":is_found
                    
                    }})

            drift_report_file_path = self.data_validation_config.drift_report_file_path
            os.makedirs(drift_report_file_path, exist_ok=False)
            write_yaml_file(drift_report_file_path, report, replace= True)
            return status
        except Exception as e:
            raise SensorException(e, sys)
            
    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            train_df = DataValidation.read_data(train_file_path)
            test_df = DataValidation.read_data(test_file_path)
            status = self.validate_number_of_columns(dataframe=train_df)
            if not status:
                error_message=f"{error_message}Train dataframe does not contain all columns.\n"
            status = self.validate_number_of_columns(dataframe=test_df)
            if not status:
                error_message=f"{error_message}Test dataframe does not contain all columns.\n"
        

            #Validate numerical columns

            status = self.is_numerical_column_exist(dataframe=train_df)
            if not status:
                error_message=f"{error_message}Train dataframe does not contain all numerical columns.\n"
            
            status = self.is_numerical_column_exist(dataframe=test_df)
            if not status:
                error_message=f"{error_message}Test dataframe does not contain all numerical columns.\n"

            if len(error_message)>0:
                raise Exception(error_message)

            status = self.detect_dataset_drift(base_df=train_df,current_df=test_df)
            

            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )

            logging.info(f"Data validation artifact: {data_validation_artifact}")

            return data_validation_artifact
            #Validate number of columns 
        except Exception as e:
            raise SensorException(e,sys)