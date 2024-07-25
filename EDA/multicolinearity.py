from statsmodels.stats.outliers_influence import variance_inflation_factor
import pandas as pd
from Data.columns import *
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


def calculate_vif(df, filename):
    """Function to calculate VIF"""
    vif_df = pd.DataFrame(data=df.columns, columns=["feature"])
    vif_df["VIF"] = [variance_inflation_factor(df.values, i) for i in range(df.shape[1])]
    vif_df.to_csv(f"../Data/Multicollinearity/vif_{filename}.csv", index=False)
    return vif_df


if __name__ == "__main__":

    scaler = StandardScaler()
    pca = PCA(n_components=10)

    # Load data
    data = pd.read_csv("../Data/cleaned_clustered_ncaa_drafted_qbs.csv")
    data.drop(columns=drop_cols, axis=1, inplace=True)
    data.drop(columns=[i for i in dependent_variables.keys()], axis=1, inplace=True)

    # Check VIF for regular data
    normal_vif_df = calculate_vif(data, "regular")

    # Check VIF for scaled data
    scaled_data = pd.DataFrame(scaler.fit_transform(data), columns=data.columns)
    scaled_vif_data = calculate_vif(scaled_data, "scaled")

    # Check VIF for scaled and PCA data
    pca_scaled_data = pd.DataFrame(pca.fit_transform(scaled_data), columns=[f"pc{i+1}" for i in range(0, pca.n_components)])
    pca_scaled_vif_data = calculate_vif(pca_scaled_data, "scaled_pca")

