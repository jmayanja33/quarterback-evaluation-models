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
        predictions.append(predictor.predict())
        columns.append(variable)

    # Save predictions
    predictor = Predictor("cluster")
    prediction_df = pd.DataFrame(np.array(predictions).T, columns=columns)
    predictor.save_predictions(prediction_df)

    # Find cosine similarity
    predictor.similarity()

