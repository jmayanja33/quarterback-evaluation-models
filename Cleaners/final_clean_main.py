from cluster_edits import edits
from Logs.logger import Logger
import pandas as pd


def assign_cluster(ncaa_data, cluster_data):
    """Function to assign clusters to each player in the cleaned NCAA data"""
    clusters = []
    players = set(cluster_data["player"])
    edited_players = edits.keys()

    # Iterate through data and assign clusters
    for i in range(len(ncaa_data)):
        player = ncaa_data["player"][i]

        # Case if the player's cluster has been edited
        if player in edited_players:
            cluster = edits[player]
            clusters.append(cluster)

        # Case if the player is old enough to be clustered
        elif player in players:
            cluster_index = list(cluster_data["player"]).index(player)
            cluster = list(cluster_data["cluster"])[cluster_index]
            clusters.append(cluster)

        # Case if the player is too young to be clustered and in the test set
        else:
            clusters.append(-999)

    # Add clusters to data
    ncaa_data["cluster"] = clusters
    return ncaa_data


if __name__ == '__main__':

    # Initialize Logger
    logger = Logger()

    # Load data
    logger.info("Loading Data")
    cleaned_data_path = "../Data/cleaned_ncaa_drafted_qbs.csv"
    cluster_data_path = "../Data/ClusterResults/K-Means/nfl_qb_clusters_normalized.csv"

    ncaa_df = pd.read_csv(cleaned_data_path)
    cluster_df = pd.read_csv(cluster_data_path)

    # Add clusters to data
    logger.info("Assigning clusters to data")
    clustered_ncaa_df = assign_cluster(ncaa_df, cluster_df)
    x = clustered_ncaa_df.copy()
    x.sort_values(by=["cluster", "player"], inplace=True)

    # Save data
    logger.info("Saving data")
    clustered_ncaa_df.to_csv("../Data/cleaned_clustered_ncaa_drafted_qbs.csv", index=False)

