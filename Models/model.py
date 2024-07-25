from sklearn.metrics import accuracy_score, r2_score, root_mean_squared_error
from sklearn.model_selection import GridSearchCV
from Helpers.helpers import make_directory
from Data.columns import *
from Logs.logger import Logger
import pandas as pd
import numpy as np
import pickle

np.random.seed(33)


def calculate_adj_r2(r2, data):
    """Function to calculate adjusted r-squared"""
    try:
        num_observations = len(data)
        num_features = len(data.columns)
        return 1 - (1-r2) * (num_observations-1)/(num_observations-num_features-1)
    except AttributeError:
        data_copy = pd.DataFrame(data)
        num_observations = len(data_copy)
        num_features = len(data_copy.columns)
        return 1 - (1 - r2) * (num_observations - 1) / (num_observations - num_features - 1)
    except ZeroDivisionError:
        return "ZeroDivisionError"


def load_data(dependent_variable):
    """Function to load data"""
    data_path = f"../../Data/TrainingData/{dependent_variable}"
    X_train = pd.read_csv(f"{data_path}/X_train.csv")
    X_test = pd.read_csv(f"{data_path}/X_test.csv")
    y_train = pd.read_csv(f"{data_path}/y_train.csv")
    y_test = pd.read_csv(f"{data_path}/y_test.csv")

    # Remove player name and id
    X_train.drop(columns=drop_cols, axis=1, inplace=True)
    X_test.drop(columns=drop_cols, axis=1, inplace=True)

    return X_train, X_test, y_train, y_test


class Model:

    def __init__(self, dependent_variable, model_type):
        self.logger = Logger()
        self.model = None
        self.model_type = model_type
        self.dependent_variable = dependent_variable
        self.X_train, self.X_test, self.y_train, self.y_test = load_data(dependent_variable)
        self.best_params = None

        self.initialize_directories()

    def initialize_directories(self):
        """Function to initialize directories to hold results"""
        make_directory(self.dependent_variable)
        make_directory(f"{self.dependent_variable}", "Results")
        make_directory(f"{self.dependent_variable}", "TrainingStats")

    def fit(self):
        """Function to fit a model"""
        self.logger.info(f"Fitting model for {self.model_type} {self.dependent_variable} model")
        self.model.fit(self.X_train, self.y_train)
        predictions = self.model.predict(self.X_test)
        self.summary_report(predictions)
        self.save_model()

    def grid_search(self, model_object=None, param_grid=None, scoring=None):
        """Function to perform grid search cross validation"""
        self.logger.info(f"Performing 5 fold cross validation for {self.model_type} {self.dependent_variable} model")
        params_model = GridSearchCV(estimator=model_object, param_grid=param_grid, scoring=scoring,
                                    verbose=10, n_jobs=-1, cv=5)
        params_model.fit(self.X_train, self.y_train)
        self.best_params = params_model.best_params_

    def predict(self):
        """Function to predict a model"""
        return self.model.predict(self.X_test)

    def save_model(self):
        """Function to save a model"""
        with open(f"{self.dependent_variable}/model.pkl", "wb") as pkl_file:
            pickle.dump(self.model, pkl_file)
            pkl_file.close()

    def summary_report(self, predictions):
        """Function to write a summary report"""
        self.logger.info(f"Writing summary report for {self.model_type} {self.dependent_variable} model")

        content = f"""-----SUMMARY REPORT-----
        
- Best Params: {self.best_params}
        """

        # Calculate regression metrics if regression is performed
        if dependent_variables[self.dependent_variable] == "regression":
            rmse = round(root_mean_squared_error(self.y_test, predictions), 4)
            content += f"\n\n- RMSE: {rmse}"
        else:
            accuracy = round(accuracy_score(self.y_test, predictions), 4)
            content += f"\n\n- Accuracy: {accuracy}"

        # Calculate base metrics
        r_squared = round(r2_score(self.y_test, predictions), 4)
        adj_r_squared = round(calculate_adj_r2(r_squared, self.X_test), 4)

        # Write base metrics to report
        content += f"""\n- R-Squared Score: {r_squared}\n- Adj. R-Squared Score: {adj_r_squared}"""

        # Write to file
        file = open(f"{self.dependent_variable}/Results/summary_report.txt", "w")
        file.write(content)
        file.close()

