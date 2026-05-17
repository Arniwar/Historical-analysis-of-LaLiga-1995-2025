"""
Exercici 7: clustering amb KMeans sobre el resum per equip.

Escullo les cinc variables numèriques del resum, les escalo amb
``StandardScaler`` perquè cap domini per escala, i entreno KMeans amb
``random_state`` fix per poder reproduir resultats. Deso el model en pickle sota
``model/``. Per visualitzar, pinto cada clúster d’un color i etiqueto cada punt
amb el nom de l’equip.
"""

from pathlib import Path
import pickle

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

import config


def model_clusters(df: pd.DataFrame, num_clusters: int) -> dict:
    """
    Entreno KMeans sobre les columnes estandarditzades i deso scaler + model.

    Utilitzo ``n_init=10`` (valor explícit recomanat en versions recents de
    scikit-learn) per evitar avisos de paràmetre per defecte.
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
    """Copio el dataframe i hi afegeixo ``cluster`` amb les etiquetes del model."""
    df = df.copy()
    df["cluster"] = kmeans.labels_

    return df


def plot_clusters(df: pd.DataFrame, attr1: str, attr2: str) -> None:
    """
    Scatter per clúster; per cada punt poso el text del nom de l’equip.

    El nom del fitxer inclou nombre de clústers, atributs i el meu identificador
    per demostrar que la figura és de la meva execució.
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
    Carrego un model desat i prediu el clúster d’una fila nova.

    Aplico el mateix ``scaler`` que a l’entrenament amb ``transform`` (no
    ``fit_transform``) per coherència dimensional.
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

'''
Responeu a les següents preguntes: amb 4 clústers, quants equips hi ha en el clúster dels millors? Quins són?
Hi ha 2 equips, el Barcelona i el Real Madrid
'''