import sys, os
from dataclasses import dataclass
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, StandardScaler, OneHotEncoder

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object



@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path : str = os.path.join('artifacts','preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformation_object(self):
        try:
            num_cols = ['writing_score','reading_score']
            cat_cols = ['gender','race_ethnicity', 'parental_level_of_education',
                        'lunch','test_preparation_course']
            
            # Transformation of numerical columns
            num_pipeline = Pipeline([
                ('imputer',SimpleImputer(strategy='median')),
                ('scaler',StandardScaler())
            ])
            logging.info('Numerical transformation completed')
            # Categorical Variable transformation
            cat_pipeline = Pipeline([
                ('imputer',SimpleImputer(strategy='most_frequent')),
                ('ohe',OneHotEncoder()),
                ('scaler',StandardScaler(with_mean=False))
            ])

            logging.info('Categorical transformation completed')

            # ColumnTransformation
            preprocessor = ColumnTransformer([
                ("num_pipe",num_pipeline,num_cols),
                ('cat_pipe',cat_pipeline,cat_cols)
            ])

            return preprocessor
            logging.info('Data transformation object created')

        except Exception as e:
            raise CustomException(e,sys)
        

    def initiate_data_transformation(self,train_path,test_path):

        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            # Get preprocessor object(pkl file)
            prprocessor_obj = self.get_data_transformation_object()

            target_col = 'math_score'
                        
            # X_train,y_train
            input_feature_train_df = train_df.drop(target_col,axis=1)
            target_feature_train_df = train_df[target_col]

            # X_test,y_test
            input_feature_test_df = test_df.drop(target_col,axis=1)
            target_feature_test_df = test_df[target_col]

            # applying transformation steps on above data
            input_feature_train_arr = prprocessor_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = prprocessor_obj.fit_transform(input_feature_test_df)

            train_arr = np.c_[input_feature_train_arr,np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr,np.array(target_feature_test_df)]

            logging.info('Data Transformation completed and got the training and test array as output.')


            # Saving the transformation object
            save_object(file_path = self.data_transformation_config.preprocessor_obj_file_path, obj=prprocessor_obj)

            return (train_arr,
                    test_arr,
                    self.data_transformation_config.preprocessor_obj_file_path
            )


        except Exception as e:
            raise CustomException(e,sys)

        