import pandas as pd
from hdbscan import HDBSCAN
from kmeans import KMeans
import warnings

warnings.filterwarnings("ignore")


if __name__ == '__main__':

    # Load data
    data = pd.read_csv('../data/cleaned_nfl_draft_qbs.csv')

    # Initialize engines
    hdbscan = HDBSCAN(data)
    kmeans = KMeans(data)

    # Fit HDBSCAN models
    hdbscan.fit()
    hdbscan.fit(normalize=True)

    # Fit KMeans models
    kmeans.fit(k=5)
    kmeans.fit(k=8, normalize=True)

