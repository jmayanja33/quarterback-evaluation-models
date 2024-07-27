from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from Data.columns import dependent_variables
from Models.model import Model


class RandomForest(Model):

    def __init__(self, dependent_variable):
        model_type = "RandomForest"
        super().__init__(dependent_variable, model_type)

        # Initialize a regressor or classifier
        self.initialize_model()

    def initialize_model(self):
        """Function to initialize a model"""
        # Initialize a regressor model
        if dependent_variables[self.dependent_variable] == "regression":
            if self.best_params is None:
                self.logger.info(f"Initializing {self.model_type} {self.dependent_variable} model")
                self.model = RandomForestRegressor(random_state=33)
            else:
                self.logger.info(f"Configuring {self.model_type} {self.dependent_variable} model with best parameters")
                self.model = RandomForestRegressor(**self.best_params, random_state=33)
        # Initialize a classifier
        else:
            if self.best_params is None:
                self.logger.info(f"Initializing {self.model_type} {self.dependent_variable} model")
                self.model = RandomForestClassifier(random_state=33)
            else:
                self.logger.info(f"Configuring {self.model_type} {self.dependent_variable} model with best parameters")
                self.model = RandomForestClassifier(**self.best_params, random_state=33)

    def fit(self):
        """Function to find the best parameters with gridsearch CV and then fit a model"""
        self.grid_search()
        super().fit()

    def grid_search(self, model_object=None, param_grid=None, scoring=None):
        """Function to fit a model with gridsearch cross-validation"""

        # Initialize param grid and demo model
        param_grid = {
            "n_estimators": [i for i in range(100, 600, 100)],
            "max_depth": [i for i in range(1, 11, 1)],
        }

        # Initialize a regressor or classifier
        if dependent_variables[self.dependent_variable] == "regression":
            model = RandomForestRegressor(random_state=33)
            scoring = "neg_mean_squared_error"
        else:
            model = RandomForestClassifier(random_state=33)
            scoring = "accuracy"

        # Run Grid Search CV
        super().grid_search(model, param_grid, scoring)

        # Recreate model with best params
        self.initialize_model()
