"""Exercici 1: càrrega del dataset i anàlisi exploratòria."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

import config


def load_and_eda(file_path: str) -> pd.DataFrame:
    """
    Carrega el dataset de LaLiga i elimina les columnes del descans.

    Args:
        file_path: Ruta del fitxer CSV.

    Returns:
        pd.DataFrame: Dataset sense les columnes HTHG, HTAG i HTR.
    """
    data = pd.read_csv(file_path)
    data = data.drop(columns=["HTHG", "HTAG", "HTR"])

    return data


def plot_home_away_goals(data: pd.DataFrame) -> None:
    """
    Genera una figura amb dos boxplots per comparar els gols locals i visitants.

    Args:
        data: DataFrame amb les dades dels partits.
    """
    Path(config.IMG_PATH).mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.boxplot(data["FTHG"].dropna())
    plt.title("Distribució de gols locals")
    plt.ylabel("Nombre de gols")
    plt.xticks([1], ["FTHG"])

    plt.subplot(1, 2, 2)
    plt.boxplot(data["FTAG"].dropna())
    plt.title("Distribució de gols visitants")
    plt.ylabel("Nombre de gols")
    plt.xticks([1], ["FTAG"])

    plt.suptitle("Distribució de gols locals i visitants")
    plt.tight_layout()

    plt.savefig(
        f"{config.IMG_PATH}/grafica_ex1_"
        f"{config.nom_alumne}_{config.date_time}.png"
    )
    plt.close()