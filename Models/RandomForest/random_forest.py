from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from Data.columns import dependent_variables
from Models.model import Model


class RandomForest(Model):

    def __init__(self, dependent_variable):
        model_type = "RandomForest"
        # Initialize a regressor or classifier
        if dependent_variables[dependent_variable] == "regression":
            model = RandomForestRegressor(max_depth=5)
        else:
            model = RandomForestClassifier(max_depth=5)

        super().__init__(dependent_variable, model_type, model)

        # Initialize a regressor or classifier
        if dependent_variables[self.dependent_variable] == "regression":
            self.model = RandomForestRegressor(max_depth=5)
        else:
            self.model = RandomForestClassifier(max_depth=5)

