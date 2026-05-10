"""Exercici 7: model de clústers amb KMeans."""

from pathlib import Path
import pickle

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

import config


def model_clusters(df: pd.DataFrame, num_clusters: int) -> dict:
    """
    Entrena un model KMeans amb les dades resumides dels equips.

    Args:
        df: DataFrame amb les dades dels equips.
        num_clusters: Nombre de clústers del model.

    Returns:
        dict: Diccionari amb scaler, num_clusters i kmeans.
    """
    Path(config.MODEL_PATH).mkdir(parents=True, exist_ok=True)

    selected_columns = [
        "points",
        "home_goals",
        "away_goals",
        "total_goals",
        "stadium_capacity",
    ]

    x_values = df[selected_columns].copy()

    scaler = StandardScaler()
    x_scaled = scaler.fit_transform(x_values)

    kmeans = KMeans(
        n_clusters=num_clusters,
        random_state=42,
        n_init=10,
    )
    kmeans.fit(x_scaled)

    model_data = {
        "scaler": scaler,
        "num_clusters": num_clusters,
        "kmeans": kmeans,
    }

    with open(f"{config.MODEL_PATH}/model_{num_clusters}.pkl", "wb") as file:
        pickle.dump(model_data, file)

    return model_data


def assignacio_clusters(df: pd.DataFrame, kmeans: KMeans) -> pd.DataFrame:
    """
    Afegeix al dataframe una columna amb el clúster assignat.

    Args:
        df: DataFrame amb les dades dels equips.
        kmeans: Model KMeans entrenat.

    Returns:
        pd.DataFrame: DataFrame amb la columna cluster.
    """
    df = df.copy()
    df["cluster"] = kmeans.labels_

    return df


def plot_clusters(df: pd.DataFrame, attr1: str, attr2: str) -> None:
    """
    Genera un gràfic de dispersió dels equips segons dos atributs.

    Args:
        df: DataFrame amb les dades dels equips i la columna cluster.
        attr1: Atribut que es mostra a l'eix X.
        attr2: Atribut que es mostra a l'eix Y.
    """
    Path(config.IMG_PATH).mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(9, 6))

    for cluster in sorted(df["cluster"].unique()):
        cluster_data = df[df["cluster"] == cluster]

        plt.scatter(
            cluster_data[attr1],
            cluster_data[attr2],
            label=f"Clúster {cluster}",
        )

        for _, row in cluster_data.iterrows():
            plt.text(
                row[attr1],
                row[attr2],
                row["team"],
                fontsize=8,
            )

    plt.title(f"Clústers segons {attr1} i {attr2}")
    plt.xlabel(attr1)
    plt.ylabel(attr2)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    num_clusters = df["cluster"].nunique()

    plt.savefig(
        f"{config.IMG_PATH}/grafica_ex7_{num_clusters}_clusters_"
        f"{attr1}_{attr2}_{config.nom_alumne}_{config.date_time}.png"
    )
    plt.close()


def predict_new_team_cluster(
    model_path: str,
    new_team_data: pd.DataFrame,
) -> int:
    """
    Carrega un model entrenat i prediu el clúster d'un nou equip.

    Args:
        model_path: Ruta del fitxer pickle del model entrenat.
        new_team_data: DataFrame amb les dades del nou equip.

    Returns:
        int: Clúster assignat al nou equip.
    """
    selected_columns = [
        "points",
        "home_goals",
        "away_goals",
        "total_goals",
        "stadium_capacity",
    ]

    with open(model_path, "rb") as file:
        model_data = pickle.load(file)

    scaler = model_data["scaler"]
    kmeans = model_data["kmeans"]

    x_new = new_team_data[selected_columns]
    x_new_scaled = scaler.transform(x_new)

    predicted_cluster = kmeans.predict(x_new_scaled)

    return int(predicted_cluster[0])