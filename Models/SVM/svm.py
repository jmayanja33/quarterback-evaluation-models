from sklearn.svm import SVR, SVC
from Data.columns import dependent_variables
from Models.model import Model


class SVM(Model):

    def __init__(self, dependent_variable):
        model_type = "SVM"
        super().__init__(dependent_variable, model_type)

        # Initialize a regressor or classifier
        self.initialize_model()

    def initialize_model(self):
        """Function to initialize a model"""
        # Initialize a regressor model
        if dependent_variables[self.dependent_variable] == "regression":
            if self.best_params is None:
                self.logger.info(f"Initializing {self.model_type} {self.dependent_variable} model")
                self.model = SVR()
            else:
                self.logger.info(f"Configuring {self.model_type} {self.dependent_variable} model with best parameters")
                self.model = SVR(**self.best_params)
        # Initialize a classifier
        else:
            if self.best_params is None:
                self.logger.info(f"Initializing {self.model_type} {self.dependent_variable} model")
                self.model = SVC()
            else:
                self.logger.info(f"Configuring {self.model_type} {self.dependent_variable} model with best parameters")
                self.model = SVC(**self.best_params)

    def fit(self):
        """Function to find the best parameters with gridsearch CV and then fit a model"""
        self.grid_search()
        super().fit()

    def grid_search(self, model_object=None, param_grid=None, scoring=None):
        """Function to fit a model with gridsearch cross-validation"""

        # Initialize param grid and demo model
        param_grid = {
            "C": [0.1, 1, 10, 100, 1000],
            "kernel": ["linear", "poly", "rbf"],
            "gamma": ["scale", "auto"],
        }

        # Initialize a regressor or classifier
        if dependent_variables[self.dependent_variable] == "regression":
            model = SVR()
            scoring = "neg_mean_squared_error"
        else:
            model = SVC()
            scoring = "accuracy"

        # Run Grid Search CV
        super().grid_search(model, param_grid, scoring)

        # Recreate model with best params
        self.initialize_model()
