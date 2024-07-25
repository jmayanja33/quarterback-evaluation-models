from Data.columns import *
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from Logs.logger import Logger
from tensorflow import keras
from scipy.spatial.distance import cosine
import pandas as pd
import numpy as np
import pickle


def load_data(dependent_variable="cluster", filepath=None, similarity=False):
    """Function to load data"""
    scaler = StandardScaler()
    pca = PCA(n_components=10)

    if filepath is None:
        filepath = f"../Data/TrainingData/{dependent_variable}/young_qb_test_data.csv"
    test_data = pd.read_csv(filepath)

    # Return data if not being used for predictions
    if similarity:
        return test_data

    # Remove player name and id
    test_data.drop(columns=drop_cols, axis=1, inplace=True)
    test_data.drop(columns=[i for i in dependent_variables.keys()], axis=1, inplace=True)

    # Scale and normalize features
    test_data = pd.DataFrame(scaler.fit_transform(test_data), columns=test_data.columns)
    test_data = pd.DataFrame(pca.fit_transform(test_data), columns=[f"pc{i + 1}" for i in range(0, pca.n_components)])

    return test_data


def load_model(dependent_variable):
    """Function to load the best model for the corresponding dependent variable"""
    model_type = best_models[dependent_variable]

    # Load keras model
    if model_type == "ANN":
        model_path = f"../Models/{model_type}/{dependent_variable}/model.keras"
        model = keras.models.load_model(model_path)
        return model

    # Load sklearn model
    else:
        model_path = f"../Models/{model_type}/{dependent_variable}/model.pkl"
        with open(model_path, "rb") as pkl_file:
            model = pickle.load(pkl_file)
            pkl_file.close()

        return model


def save_cosine_similarities(cosine_similarities):
    """Function to save cosine similarities"""
    columns = ["player", "most_similar_1", "most_similar_1_value", "most_similar_2",
               "most_similar_2_value", "most_similar_3", "most_similar_3_value"]

    # Extract tuples
    formatted_cosine_similarities = []
    for i in cosine_similarities:
        row = [i[0]]
        for j in i[1]:
            row.append(j[0])
            row.append(j[1])
        formatted_cosine_similarities.append(row)

    # Create data frame
    df = pd.DataFrame(formatted_cosine_similarities, columns=columns)
    df.to_csv("../Data/Predictions/cosine_similarities.csv")


class Predictor:

    def __init__(self, dependent_variable):
        self.logger = Logger()
        self.dependent_variable = dependent_variable
        self.data = load_data(dependent_variable)
        self.model = load_model(dependent_variable)

    def predict(self):
        """Function to make predictions"""
        self.logger.info(f"Making predictions for {self.dependent_variable}")

        # Make predictions
        predictions = self.model.predict(self.data)
        if dependent_variables[self.dependent_variable] == "regression":
            predictions = [round(float(i), 0) for i in predictions]
        else:
            predictions = [np.argmax(i) for i in predictions]
        return predictions

    def similarity(self):
        """Function to find cosine similarity between two players"""

        cosine_similarities = []
        removals = {"player", "player_id", "years_missing", "first_team_all_pro_selections", "pro_bowl_selections",
                    "number_of_years_as_a_starter", "weighted_career_approximate_value", "cluster"}

        # Load data
        young_qb_data = load_data(similarity=True)
        old_qb_data = load_data(filepath="../Data/cleaned_clustered_ncaa_drafted_qbs.csv", similarity=True)
        old_qb_data = old_qb_data[old_qb_data["cluster"] != -999]
        old_qb_data.reset_index(drop=True, inplace=True)

        # Iterate through all young qbs
        for i in range(len(young_qb_data)):

            # Find player
            young_qb = young_qb_data["player"][i]
            young_qb_vector = np.array(young_qb_data[[col for col in young_qb_data.columns if col not in removals]].iloc[i])

            # Initialize structure to hold top 3 similarities
            top_three = [(None, 0) for i in range(3)]

            # Iterate through all old qbs
            for j in range(len(old_qb_data)):

                # Find player
                old_qb = old_qb_data["player"][j]
                self.logger.info(f"Calculating cosine similarity between {young_qb} and {old_qb}; Total Progress: {i+1}/{len(young_qb_data)}; QB Progress: {j+1}/{len(old_qb_data)}")
                old_qb_vector = np.array(old_qb_data[[col for col in old_qb_data.columns if col not in removals]].iloc[j])

                # Calculate similarity
                cosine_similarity = 1 - cosine(young_qb_vector, old_qb_vector)

                # Save top 3 cosine similarities
                top_three.append((old_qb, cosine_similarity))
                top_three.sort(key=lambda x: x[1], reverse=True)
                top_three = top_three[:3]
                
            # Save top 3
            cosine_similarities.append([young_qb, top_three])

        # Save similarities
        self.logger.info("Saving cosine similarities")
        save_cosine_similarities(cosine_similarities)

    def save_predictions(self, predictions):
        """Function to save predictions"""
        self.logger.info("Saving predictions")
        player_data = load_data(dependent_variable=self.dependent_variable, similarity=True)
        predictions["player"] = list(player_data["player"])
        predictions.to_csv("../Data/Predictions/predictions.csv", index=False)

