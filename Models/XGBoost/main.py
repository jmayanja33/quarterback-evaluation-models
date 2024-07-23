from xg_boost import XGBoost
from Data.columns import dependent_variables


DEPENDENT_VARIABLES = [i for i in dependent_variables.keys()]


if __name__ == "__main__":

    for variable in DEPENDENT_VARIABLES:

        # Initialize Random Forest model
        model = XGBoost(variable)
        model.fit()
