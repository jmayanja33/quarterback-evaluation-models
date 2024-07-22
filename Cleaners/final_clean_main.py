from cluster_edits import edits
from Logs.logger import Logger
from Data.columns import *
import pandas as pd


def assign_variables(variable, ncaa_data, variable_data):
    """Function to assign dependent variables to each player in the cleaned NCAA data"""
    stats = []
    players = set(variable_data["player"])
    edited_players = edits.keys()

    # Iterate through data and assign clusters
    for i in range(len(ncaa_data)):
        player = ncaa_data["player"][i]

        # Case if the player's cluster has been edited
        if player in edited_players and variable == 'cluster':
            cluster = edits[player]
            stats.append(cluster)

        # Case if the player is old enough to be clustered
        elif player in players:
            player_index = list(variable_data["player"]).index(player)
            stat = list(variable_data[variable])[player_index]
            stats.append(stat)

        # Case if the player is too young to be clustered and in the test set
        else:
            stats.append(-999)

    # Add clusters to data
    ncaa_data[variable] = stats
    return ncaa_data


if __name__ == '__main__':

    # Initialize Logger
    logger = Logger()

    # Load data
    logger.info("Loading Data")
    cleaned_data_path = "../Data/cleaned_ncaa_drafted_qbs.csv"
    cluster_data_path = "../Data/ClusterResults/K-Means/nfl_qb_clusters_normalized.csv"
    nfl_data_path = "../Data/cleaned_nfl_draft_qbs.csv"

    ncaa_df = pd.read_csv(cleaned_data_path)
    cluster_df = pd.read_csv(cluster_data_path)
    nfl_df = pd.read_csv(nfl_data_path)

    # Add dependent variables to data
    for variable in dependent_variables.keys():
        logger.info(f"Assigning {variable} to data")
        if variable == 'cluster':
            ncaa_df = assign_variables(variable, ncaa_df, cluster_df)
        else:
            ncaa_df = assign_variables(variable, ncaa_df, nfl_df)
        # debug = final_ncaa_df.copy()
        # debug.sort_values(by=["cluster", "player"], inplace=True)

    # Save data
    logger.info("Saving data")
    ncaa_df.to_csv("../Data/cleaned_clustered_ncaa_drafted_qbs.csv", index=False)

