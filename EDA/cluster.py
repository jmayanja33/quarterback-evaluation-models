from Logs.logger import Logger
from matplotlib import pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from clustering_helpers import *
import pandas as pd

class Cluster:

    def __init__(self, data):
        """Base class for clustering objects"""
        self.drop_cols = [
            "year", "position", "player_id", "player", "team", "round", "pick", "final_year", "age"
        ]
        self.data = data[data["year"] < 2023]
        self.data.reset_index(drop=True, inplace=True)
        self.model = None
        self.model_type = None
        self.logger = Logger()
        self.logger.info(f"Initializing {self.model_type} engine")

    def fit(self, normalize=False):
        """Function to fit a model"""

        # Remove categorical clusters
        fit_data = self.data.drop(columns=self.drop_cols, axis=1)

        # Normalize and cluster data
        if normalize:
            fit_data = self.normalize(fit_data)

        # Cluster data
        self.logger.info(f"Fitting data with {self.model_type}; Normalized: {normalize}")
        self.model.fit(fit_data)
        fit_data["cluster"] = self.model.labels_
        self.data["cluster"] = self.model.labels_

        # Cluster data and save results
        self.plot(fit_data, normalize=normalize)
        self.save_clusters(fit_data, normalize=normalize)

    def save_clusters(self, data, normalize):
        """Function to save clusters"""

        self.logger.info(f"Saving results for {self.model_type} to a csv file; Normalized: {normalize}")

        # Initialize results directory
        make_directory("../Data/ClusterResults", f"{self.model_type.replace(' ', '')}")

        # Set filename
        if normalize:
            # Add missing columns
            for column in self.drop_cols:
                data[column] = self.data[column]

            # Set filename and save data
            filename = f"../Data/ClusterResults/{self.model_type.replace(' ', '')}/nfl_qb_clusters_normalized.csv"
            data.to_csv(filename, index=False)

        else:
            # Set filename and save data
            filename = f"../Data/ClusterResults/{self.model_type.replace(' ', '')}/nfl_qb_clusters.csv"
            self.data.to_csv(filename, index=False)

    def plot(self, data, normalize):
        """Function to plot clusters"""

        # Transform data with PCA
        pca_data = self.pca(data)

        self.logger.info(f"Plotting results for {self.model_type}; Normalized: {normalize}")

        # Initialize figure
        plt.figure(figsize=(10, 10))
        plt.xlabel("Principal Component 1")
        plt.ylabel("Principal Component 2")

        # Plot data
        x_data = pca_data["pc1"]
        y_data = pca_data["pc2"]
        cluster = pca_data["cluster"]
        scatter = plt.scatter(x_data, y_data, c=cluster, cmap="plasma")

        # Configure legend
        handles, labels = scatter.legend_elements()
        plt.legend(handles, labels, title="Cluster")

        # Initialize plot directory
        make_directory("../Data/ClusterPlots", f"{self.model_type.replace(' ', '')}")

        # Set filename
        if normalize:
            plt.title(f"{self.model_type} NFL Quarterback Clusters (Normalized)")
            filename = f"../Data/ClusterPlots/{self.model_type.replace(' ', '')}/nfl_qb_clusters_normalized.png"
        else:
            plt.title(f"{self.model_type} NFL Quarterback Clusters")
            filename = f"../Data/ClusterPlots/{self.model_type.replace(' ', '')}/nfl_qb_clusters.png"

        # Save figure
        plt.savefig(filename)
        plt.clf()

    def normalize(self, data):
        """Function to normalize data"""
        self.logger.info("Normalizing data")
        scaler = StandardScaler()
        normalized_data = scaler.fit_transform(data)
        return pd.DataFrame(normalized_data, columns=data.columns)

    def pca(self, data):
        """Function to perform principal component analysis on the data"""
        self.logger.info("Reducing data to 2 Dimensions with PCA for plotting")

        # Format data
        clusters = data["cluster"]
        pca_data = data.drop(columns=["cluster"], axis=1)

        # Fit PCA to 2D
        engine = PCA(n_components=2)
        pca_data = pd.DataFrame(engine.fit_transform(pca_data), columns=["pc1", "pc2"])

        # Re-add clusters
        pca_data["cluster"] = clusters

        return pca_data





