from ann import ANN
from Data.columns import dependent_variables
import warnings

warnings.filterwarnings("ignore")


DEPENDENT_VARIABLES = [i for i in dependent_variables.keys()]


if __name__ == "__main__":

    for variable in DEPENDENT_VARIABLES:

        # Initialize neural network
        model = ANN(variable)
        model.fit()
