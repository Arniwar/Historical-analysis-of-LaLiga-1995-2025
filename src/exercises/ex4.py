"""
Exercici 4: resultat final del partit (FTR).

Compto victòries locals (H), visitants (A) i empats (D). Utilitzo ``reindex``
amb l’ordre [H, A, D] perquè el gràfic i la taula mostrin sempre les tres
categories encara que alguna tingui zero partits (evito desalineacions).
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

import config


def FTR(data: pd.DataFrame) -> pd.DataFrame:
    """
    Agrupo per ``FTR`` i reindexo a H, A, D.

    Així mantinc l’ordre lògic del problema i les etiquetes del gràfic coincideixen
    amb el significat de cada codi.
    """
    ftr = data["FTR"].value_counts().reindex(["H", "A", "D"]).reset_index()
    ftr.columns = ["resultat", "num_partits"]

    return ftr


def plot_FTR(ftr: pd.DataFrame) -> None:
    """Barres amb etiquetes humanes al eix X (local, visitant, empat)."""
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
