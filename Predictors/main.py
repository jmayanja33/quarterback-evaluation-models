from predictor import Predictor
from Data.columns import dependent_variables
import pandas as pd
import numpy as np


if __name__ == "__main__":

    predictions = []
    columns = []

    # Iterate through each model and make predictions
    for variable in dependent_variables.keys():
        predictor = Predictor(variable)
        predicted_values, highest_probabilities, total_probabilities = predictor.predict()
        predictions.append(predicted_values)
        columns.append(variable)

        if highest_probabilities is not None:
            predictions.append(highest_probabilities)
            columns.append("probability")

        if total_probabilities is not None:
            total_prob_df = pd.DataFrame(total_probabilities, columns=["cluster_0", "cluster_1", "cluster_2", "cluster_3",
                                                                       "cluster_4", "cluster_5"])

    # Save predictions
    predictor = Predictor("cluster")
    prediction_df = pd.DataFrame(np.array(predictions).T, columns=columns)
    predictor.save_predictions(prediction_df, total_prob_df)

    # Find cosine similarity
    predictor.similarity()

