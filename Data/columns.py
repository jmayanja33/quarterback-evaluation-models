# Dictionary which holds model types for dependent variables
dependent_variables = {
    "first_team_all_pro_selections": "regression",
    "pro_bowl_selections": "regression",
    "number_of_years_as_a_starter": "regression",
    "weighted_career_approximate_value": "regression",
    "cluster": "classification"
}

# Columns to be dropped when creating a model
drop_cols = [
    "player", "player_id", "years_missing"
]

# Dictionary which holds the best model to use for each dependent variable
best_models = {
    "first_team_all_pro_selections": "KNN",
    "pro_bowl_selections": "KNN",
    "number_of_years_as_a_starter": "RandomForest",
    "weighted_career_approximate_value": "KNN",
    "cluster": "ANN"
}