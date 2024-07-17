import pandas as pd
from Logs.logger import Logger
from sklearn.preprocessing import LabelEncoder
from helpers import *
import warnings

warnings.filterwarnings("ignore")

ncaa_path = "../Data/ncaa_drafted_qbs.csv"
nfl_path = "../Data/nfl_draft_qbs.csv"


# Main to run
if __name__ == '__main__':

    logger = Logger()
    label_encoder = LabelEncoder()

    # Load data
    logger.info("Loading data")
    ncaa_df = pd.read_csv(ncaa_path)
    nfl_df = pd.read_csv(nfl_path)

    # Add age to NCAA data
    ncaa_df["age"] = nfl_df["age"]

    # Find all players with data missing
    logger.info("Finding all players with seasons missing")
    fcs_players = find_fbs_players(ncaa_df)

    # Remove FCS players
    logger.info("Removing all players with seasons missing")
    cleaned_ncaa_df = remove_fbs(ncaa_df, fcs_players)
    cleaned_nfl_df = remove_fbs(nfl_df, fcs_players)

    # Encode string variables
    logger.info("Encoding colleges and conferences")
    colleges = cleaned_ncaa_df["college"]
    for column in ["college", "conference"]:
        cleaned_ncaa_df[column] = label_encode(label_encoder, cleaned_ncaa_df[column])

    # Save college encodings
    college_encodings = save_encodings(colleges, cleaned_ncaa_df["college"])

    # Encode college column in nfl df
    cleaned_nfl_df["college"] = [college_encodings[college] for college in cleaned_nfl_df["college"]]

    # Fill in heights/ weights
    logger.info("Filling missing height/weight data")
    cleaned_ncaa_df = fill_heights_weights(cleaned_ncaa_df)
    cleaned_nfl_df = fill_heights_weights(cleaned_nfl_df)

    # Fill in age
    logger.info("Filling in age data")
    cleaned_ncaa_df = fill_age(cleaned_ncaa_df)
    cleaned_nfl_df = fill_age(cleaned_nfl_df)

    # Save cleaned data
    logger.info("Saving cleaned data")
    cleaned_ncaa_df.to_csv("../Data/cleaned_ncaa_drafted_qbs.csv", index=False)
    cleaned_nfl_df.to_csv("../Data/cleaned_nfl_draft_qbs.csv", index=False)
