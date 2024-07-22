from sklearn.metrics import accuracy_score, r2_score, root_mean_squared_error


class Model:

    def __init__(self, dependent_variable):
        self.model = None
        self.dependent_variable = dependent_variable
