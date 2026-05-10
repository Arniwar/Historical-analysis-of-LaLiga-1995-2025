"""Exercici 4: partits guanyats a casa, fora i empats."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

import config


def FTR(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula el nombre de victòries locals, visitants i empats.

    Args:
        data: DataFrame amb les dades dels partits.

    Returns:
        pd.DataFrame: DataFrame amb les columnes resultat i num_partits.
    """
    ftr = data["FTR"].value_counts().reindex(["H", "A", "D"]).reset_index()
    ftr.columns = ["resultat", "num_partits"]

    return ftr


def plot_FTR(ftr: pd.DataFrame) -> None:
    """
    Genera un gràfic de barres amb els resultats finals dels partits.

    Args:
        ftr: DataFrame amb les columnes resultat i num_partits.
    """
    Path(config.IMG_PATH).mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(7, 5))

    plt.bar(
        ftr["resultat"],
        ftr["num_partits"],
    )

    plt.title("Resultat final dels partits")
    plt.xlabel("Resultat final")
    plt.ylabel("Nombre de partits")
    plt.xticks(
        ticks=[0, 1, 2],
        labels=["H - Local", "A - Visitant", "D - Empat"],
    )
    plt.tight_layout()

    plt.savefig(
        f"{config.IMG_PATH}/grafica_ex4_"
        f"{config.nom_alumne}_{config.date_time}.png"
    )
    plt.close()