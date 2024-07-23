from random_forest import RandomForest

DEPENDANT_VARIABLES = ["cluster"]


if __name__ == "__main__":

    for variable in DEPENDANT_VARIABLES:

        # Initialize Random Forest model
        model = RandomForest(variable)
        model.fit()
