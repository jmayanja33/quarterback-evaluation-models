from sklearn.cluster import HDBSCAN as hdb
from cluster import Cluster


class HDBSCAN(Cluster):

    def __init__(self, data):
        super().__init__(data)
        self.model = hdb()
        self.model_type = "HDBSCAN"
