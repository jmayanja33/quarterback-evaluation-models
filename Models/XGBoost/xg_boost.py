from sklearn.metrics import accuracy_score, root_mean_squared_error
from sklearn.feature_selection import SelectFromModel
from xgboost import XGBRegressor, XGBClassifier
from Data.columns import dependent_variables
from Models.model import Model
from numpy import sort
import pickle


class XGBoost(Model):

    def __init__(self, dependent_variable):
        model_type = "XGBoost"
        super().__init__(dependent_variable, model_type)
        self.threshold = None

        # Initialize a regressor or classifier
        self.initialize_model()

    def initialize_model(self):
        """Function to initialize a model"""
        # Initialize a regressor model
        if dependent_variables[self.dependent_variable] == "regression":
            if self.best_params is None:
                self.logger.info(f"Initializing {self.model_type} {self.dependent_variable} model")
                self.model = XGBRegressor(random_state=33)
            else:
                self.logger.info(f"Configuring {self.model_type} {self.dependent_variable} model with best parameters")
                self.model = XGBRegressor(**self.best_params, random_state=33)
        # Initialize a classifier
        else:
            if self.best_params is None:
                self.logger.info(f"Initializing {self.model_type} {self.dependent_variable} model")
                self.model = XGBClassifier(random_state=33)
            else:
                self.logger.info(f"Configuring {self.model_type} {self.dependent_variable} model with best parameters")
                self.model = XGBClassifier(**self.best_params, random_state=33)

    def fit(self):
        """Function to find the best parameters with gridsearch CV and then fit a model"""
        self.find_feature_importance()
        self.grid_search()
        super().fit()

    def grid_search(self, model_object=None, param_grid=None, scoring=None):
        """Function to fit a model with gridsearch cross-validation"""

        # Initialize param grid and demo model
        param_grid = {
            "max_depth": [i for i in range(1, 10)],
            "learning_rate": [0.01, 0.1, 1],
            "n_estimators": [i for i in range(100, 500, 100)],
        }

        # Initialize a regressor or classifier
        if dependent_variables[self.dependent_variable] == "regression":
            model = XGBRegressor(random_state=33)
            scoring = "neg_mean_squared_error"
        else:
            model = XGBClassifier(random_state=33)
            scoring = "accuracy"

        # Run Grid Search CV
        super().grid_search(model, param_grid, scoring)

        # Recreate model with best params
        self.initialize_model()

    def find_feature_importance(self):
        """Function to plot and select most important features using the elbow method"""

        # Find feature significance
        if dependent_variables[self.dependent_variable] == "regression":
            model = XGBRegressor(random_state=33)
            scoring = "RMSE"
        else:
            model = XGBClassifier(random_state=33)
            scoring = "Accuracy"

        self.logger.info("Finding feature significance")
        model.fit(self.X_train, self.y_train)
        thresholds = set(sort(list(model.feature_importances_)))

        # Create a model using each feature importance as a feature threshold, pick threshold with lowest RMSE/highest accuracy
        model_thresholds = dict()
        file = open(f"{self.dependent_variable}/ThresholdEval.txt", "w")
        counter = 1

        # Iterate through thresholds
        for thresh in thresholds:
            features = SelectFromModel(estimator=model, threshold=thresh, prefit=True)
            # Transform feature sets
            features_X_train = features.transform(self.X_train)
            features_X_validation = features.transform(self.X_test)

            # Fit model
            if dependent_variables[self.dependent_variable] == "regression":
                feature_model = XGBRegressor(random_state=33)
                feature_model.fit(features_X_train, self.y_train)
                predictions = feature_model.predict(features_X_validation)
                result = root_mean_squared_error(self.y_test, predictions)
            else:
                feature_model = XGBClassifier(random_state=33)
                feature_model.fit(features_X_train, self.y_train)
                predictions = feature_model.predict(features_X_validation)
                result = accuracy_score(self.y_test, predictions)

            model_thresholds[thresh] = result

            # Save to file
            file.write(f"\n- Threshold: {thresh}  - {scoring}: {result}")
            self.logger.info(f"Evaluating feature threshold: {thresh}; - PROGRESS: {counter}/{len(thresholds)}")
            counter += 1
        file.close()

        # Find threshold that has best metric
        if scoring == "RMSE":
            best_metric = min(model_thresholds.values())
        else:
            best_metric = max(model_thresholds.values())

        for thresh in model_thresholds:
            if model_thresholds[thresh] == best_metric:
                self.threshold = thresh
                break

        # Use the best threshold for final feature selection
        significant_features = SelectFromModel(model, threshold=self.threshold, prefit=True)
        self.significant_feature_names = [self.X_train.columns[i] for i in
                                          significant_features.get_support(indices=True)]

        # Save most significant features to a file
        self.logger.info("Writing feature names and importance to a file")
        with open(f"{self.dependent_variable}/MostSignificantFeatures.pkl", "wb") as pklfile:
            pickle.dump(self.significant_feature_names, pklfile)
            pklfile.close()

        # Save second file with importance
        importance_vals = model.feature_importances_
        importance_dict = dict(sorted(
            {model.feature_names_in_[i]: str(importance_vals[i]) for i in range(len(importance_vals)) if
             importance_vals[i] >= self.threshold}.items(),
            key=lambda x: x[1], reverse=True))

        with open(f"{self.dependent_variable}/{self.dependent_variable}MostSignificantFeatureValues.txt", "w") as file:
            file.write(f"-----{self.dependent_variable.replace('_', ' ').upper()} FEATURE IMPORTANCE-----")
            for i in importance_dict.keys():
                file.write(f"\n- {i}: {importance_dict[i]}")
            file.close()

        # Update X_train and X_test with selected features
        self.X_train = significant_features.transform(self.X_train)
        self.X_test = significant_features.transform(self.X_test)
