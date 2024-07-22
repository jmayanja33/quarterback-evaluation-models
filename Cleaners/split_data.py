from sklearn.model_selection import train_test_split
from Data.columns import dependent_variables
from Helpers.helpers import make_directory
import pandas as pd

if __name__ == "__main__":

    # Load Data
    data = pd.read_csv("../Data/cleaned_clustered_ncaa_drafted_qbs.csv")
    train_data = data[data["cluster"] != -999]
    test_data = data[data["cluster"] == 999]

    # Split data for each dependent variable
    for variable in dependent_variables.keys():
        drops = [i for i in dependent_variables.keys()]
        features = train_data.drop(columns=drops)
        labels = train_data[variable]

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.10, random_state=33)

        # Make directory for data
        make_directory("../Data/TrainingData", variable)

        # Save to training data csv
        data_path = f"../Data/TrainingData/{variable}"
        X_train.to_csv(f"{data_path}/X_train.csv", index=False)
        X_test.to_csv(f"{data_path}/X_test.csv", index=False)
        y_train.to_csv(f"{data_path}/y_train.csv", index=False)
        y_test.to_csv(f"{data_path}/y_test.csv", index=False)

        # Save younger quarterback test data to csv
        test_data.reset_index(drop=True, inplace=True)
        test_data.to_csv(f"{data_path}/young_qb_test_data.csv", index=False)
