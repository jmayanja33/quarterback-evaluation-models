from predictor import Predictor
from Data.columns import dependent_variables
from Helpers.helpers import make_directory
import pandas as pd
import numpy as np


# Upcoming season
YEAR = 2024
DATA_PATH = f"../Data/FutureData/{YEAR+1}/cleaned_prospects.csv"


if __name__ == "__main__":

    predictions = []
    columns = []
    make_directory(f"../Data/FutureData/{YEAR + 1}", "Predictions")

    # Iterate through each model and make predictions
    for variable in dependent_variables.keys():
        predictor = Predictor(variable, filepath=DATA_PATH)
        predicted_values, highest_probabilities, total_probabilities = predictor.predict()
        predictions.append(predicted_values)
        columns.append(variable)

        if highest_probabilities is not None:
            predictions.append(highest_probabilities)
            columns.append("probability")

        if total_probabilities is not None:
            total_prob_df = pd.DataFrame(total_probabilities, columns=["staring_qb_0", "practice_squad_1", "backup_qb_2",
                                                                       "high_end_mobile_qb_3", "hall_of_fame_qb_4",
                                                                       "high_end_pocket_passer_5"])

    # Save predictions
    predictor = Predictor("cluster")
    prediction_df = pd.DataFrame(np.array(predictions).T, columns=columns)
    predictor.save_predictions(prediction_df, total_prob_df, year=YEAR+1)

    # Find cosine similarity
    predictor.similarity(YEAR+1)
