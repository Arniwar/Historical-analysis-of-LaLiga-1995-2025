"""
Exercici 3: distribució de gols (locals i visitants).

Per cada valor possible de gols, compto quantes vegades passa amb
``value_counts``, ordeno per índex (gols) i preparo dos DataFrames amb les
columnes ``gols`` i ``num_partits``. Després faig barres paral·leles per
visualitzar les dues distribucions.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

import config


def goal_distribution(data: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Obtinc la freqüència de cada marcador local i visitant.

    Poso ``gols`` com a índex per facilitar el plotting amb ``plt.bar`` sobre
    tots els valors enters presents al dataset.
    """
    distr_gols_locals = data["FTHG"].value_counts().sort_index().reset_index()
    distr_gols_locals.columns = ["gols", "num_partits"]
    distr_gols_locals = distr_gols_locals.set_index("gols")

    distr_gols_visitants = data["FTAG"].value_counts().sort_index().reset_index()
    distr_gols_visitants.columns = ["gols", "num_partits"]
    distr_gols_visitants = distr_gols_visitants.set_index("gols")

    return distr_gols_locals, distr_gols_visitants


def plot_goal_ditribution(
    distr_gols_locals: pd.DataFrame,
    distr_gols_visitants: pd.DataFrame,
) -> None:
    """Dos subplots de barres: un per FTHG i un altre per FTAG."""
    Path(config.IMG_PATH).mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    plt.bar(
        distr_gols_locals.index,
        distr_gols_locals["num_partits"],
    )
    plt.title("Distribució de gols locals")
    plt.xlabel("Nombre de gols")
    plt.ylabel("Nombre de partits")
    plt.xticks(distr_gols_locals.index)

    plt.subplot(1, 2, 2)
    plt.bar(
        distr_gols_visitants.index,
        distr_gols_visitants["num_partits"],
    )
    plt.title("Distribució de gols visitants")
    plt.xlabel("Nombre de gols")
    plt.ylabel("Nombre de partits")
    plt.xticks(distr_gols_visitants.index)

    plt.suptitle("Distribució de gols locals i visitants")
    plt.tight_layout()

    plt.savefig(
        f"{config.IMG_PATH}/grafica_ex3_"
        f"{config.nom_alumne}_{config.date_time}.png"
    )
    plt.close()
