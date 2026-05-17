"""
Exercici 1: càrrega del dataset i anàlisi exploratòria.

Llegeixo el CSV de partits, elimino les columnes de resultat al descans perquè
l’enunciat demana treballar només amb dades finals, i genero boxplots per
comparar visualment FTHG i FTAG. Les figures les deso amb el meu nom i la data
al nom del fitxer per identificar l’autoria de les sortides.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

import config


def load_and_eda(file_path: str) -> pd.DataFrame:
    """
    Carrego el CSV amb pandas i elimino HTHG, HTAG i HTR.

    Utilitzo ``drop`` amb noms de columnes explícits perquè el dataset quedi
    alineat amb el que demana l’exercici (només anàlisi sobre el resultat final).
    """
    data = pd.read_csv(file_path)
    data = data.drop(columns=["HTHG", "HTAG", "HTR"])

    return data


def plot_home_away_goals(data: pd.DataFrame) -> None:
    """
    Dibuixo dos boxplots (local i visitant) en una mateixa figura.

    Faig ``dropna()`` abans del boxplot per evitar advertències si hi ha valors
    buits; creo la carpeta ``img`` si encara no existeix.
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
