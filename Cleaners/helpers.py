from missing_data import *


def find_fbs_players(df):
    """Function to find player_ids of all fbs players"""
    cleaned_df = df[df["years_missing"] == 0]

    # Remove Joe Flacco and Andy Hall
    cleaned_df = cleaned_df[cleaned_df["player"] != "Joe Flacco"]
    cleaned_df = cleaned_df[cleaned_df["player"] != "Andy Hall"]
    return set(cleaned_df["player_id"])


def remove_fbs(df, player_ids):
    """Function to remove fbs players"""
    cleaned_df = df[df["player_id"].isin(player_ids)]
    cleaned_df.reset_index(drop=True, inplace=True)

    return cleaned_df


def label_encode(lec, column):
    """Function to label encode a text column"""
    return lec.fit_transform(column)


def save_encodings(original_data, encoded_data):
    """Function to save encodings to a dictionary"""
    encodings = {}

    # Map encodings
    for i, value in enumerate(original_data):
        if value not in encodings.keys():
            encodings[value] = int(encoded_data[i])

    return encodings


def fill_heights_weights(df):
    """Function to fill missing height and weight values"""
    # Filter players
    filtered_df = df[df["height"] == 0]
    filtered_df.reset_index(drop=True, inplace=True)

    # Iterate through players
    for i in range(len(filtered_df)):
        player = filtered_df["player"][i]
        player_index = list(df["player"]).index(player)

        # Find height/weight
        height = heights_weights[player]["height"]
        weight = heights_weights[player]["weight"]

        # Update data
        df["height"][player_index] = height
        df["weight"][player_index] = weight

    return df


def fill_age(df):
    """Function to fill missing age values"""
    # Filter players
    filtered_df = df[df["age"] == 0]
    filtered_df.reset_index(drop=True, inplace=True)

    # Iterate through players
    for i in range(len(filtered_df)):
        player = filtered_df["player"][i]
        player_index = list(df["player"]).index(player)

        # Find age
        age = ages[player]

        # Update data
        df["age"][player_index] = age

    return df


