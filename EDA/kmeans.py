from sklearn.cluster import KMeans as kmeans
from matplotlib import pyplot as plt
from clustering_helpers import *
from cluster import Cluster


class KMeans(Cluster):

    def __init__(self, data, k=6):
        super().__init__(data)
        self.k = k
        self.model = kmeans(n_clusters=k, random_state=33)
        self.model_type = "K-Means"

        # Plot elbows
        self.elbow_method()
        self.elbow_method(normalize=True)

    def fit(self, normalize=False, k=None):
        """Function to fit a K-Means model to a dataset"""

        # Set model
        if k is not None:
            self.k = k
            self.model = kmeans(n_clusters=k, random_state=33)

        super().fit(normalize=normalize)



    def elbow_method(self, normalize=False):
        """Function to implement the elbow method for 25 clusters"""
        self.logger.info(f"Plotting the elbow for KMeans; Normalized: {normalize}")

        # Remove categorical clusters
        fit_data = self.data.drop(columns=self.drop_cols, axis=1)

        # Normalize and cluster data
        if normalize:
            fit_data = self.normalize(fit_data)

        # Initialize within cluster sum of squares
        WCSS = []

        # Iterate through k=[1,25] and fit a model with
        for i in range(1, 25):
            model = kmeans(n_clusters=i)
            model.fit(fit_data)
            WCSS.append(model.inertia_)

        # Plot results
        self.plot_elbow(WCSS, normalize)

    def plot_elbow(self, data, normalize):
        """Function to plot the elbow"""

        # Initialize figure
        plt.figure(figsize=(10, 10))
        plt.xlabel("Principal Component 1")
        plt.ylabel("Principal Component 2")

        # Plot data
        x_data = [i for i in range(len(data))]
        y_data = data
        plt.scatter(x_data, y_data)

        # Initialize plot directory
        make_directory("../Data/ClusterPlots", f"{self.model_type.replace(' ', '')}")

        # Set filename
        if normalize:
            plt.title(f"{self.model_type} NFL Quarterback Elbow Plot (Normalized)")
            filename = f"../Data/ClusterPlots/{self.model_type.replace(' ', '')}/nfl_qb_elbow_normalized.png"
        else:
            plt.title(f"{self.model_type} NFL Quarterback Elbow Plot")
            filename = f"../Data/ClusterPlots/{self.model_type.replace(' ', '')}/nfl_qb_elbow.png"

        # Save figure
        plt.savefig(filename)
        plt.clf()

