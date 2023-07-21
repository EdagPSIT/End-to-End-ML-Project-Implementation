import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd

from sklearn.model_selection import train_test_split

from dataclasses import dataclass

from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig

# In this step of Data Ingestion, 
#   1. Create data paths for train, test, and raw data
#   2. Read the data from different sources  
#   3. Split the data into train_set and test_set using sklearn
#   4. Save the splitted data into defined path using to_csv method of pandas
#   5. Return the path objects

@dataclass
class DataIngestionConfig:
        train_data_path:str = os.path.join('artifacts','train.csv')
        test_data_path:str = os.path.join('artifacts','test.csv')
        raw_data_path:str = os.path.join('artifacts','data.csv')
    
class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()
    
    def data_ingestion_initiation(self):

        try:
            # Reading the raw data
            df = pd.read_csv('Research\Data\data.csv')
            logging.info('Read data into pandas dataframe completed.')

            # Create train data saving path
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)

            # Saving the raw data to raw_data_path
            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)

            # Splitting data into train and test
            logging.info("Train test split Initiated")

            train_set,test_set = train_test_split(df,test_size=0.2,random_state=42)

            # Saving training and test dataset to defined path
            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)

            logging.info("Data Ingestion is completed")
            
            return self.ingestion_config.train_data_path, self.ingestion_config.test_data_path

        except Exception as e:
            raise CustomException(e,sys)
    


if __name__=="__main__":
    obj = DataIngestion()
    train_data, test_data = obj.data_ingestion_initiation()

    # data transformation step
    data_transformation = DataTransformation()
    data_transformation.initiate_data_transformation(train_data,test_data)