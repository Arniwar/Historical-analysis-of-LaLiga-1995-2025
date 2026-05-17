"""
Exercici 2: partits totals jugats per equip.

Compto partits com a local amb ``value_counts`` sobre ``HomeTeam`` i com a
visitant sobre ``AwayTeam``. Després sumo les dues sèries amb ``add`` i
``fill_value=0`` per cobrir equips que només apareguin en un rol. Ordeno de
major a menor i resetejo l’índex per tenir columnes ``team`` i ``total_matches``.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

import config


def total_matches(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculo el total de partits per equip (local + visitant).

    ``add`` amb ``fill_value=0`` m’assegura que si un equip no té registres en
    una de les dues sèries, el comptador no es quedi amb NaN.
    """
    home_matches = data["HomeTeam"].value_counts()
    away_matches = data["AwayTeam"].value_counts()

    matches_team_total = home_matches.add(away_matches, fill_value=0)

    matches_team_total = (
        matches_team_total.astype(int)
        .sort_values(ascending=False)
        .reset_index()
    )

    matches_team_total.columns = ["team", "total_matches"]

    return matches_team_total


def plot_matches_team_total(matches_team_total: pd.DataFrame) -> None:
    """Gràfic de barres amb tots els equips; roto les etiquetes 90° per llegibilitat."""
    Path(config.IMG_PATH).mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(16, 7))

    plt.bar(
        matches_team_total["team"],
        matches_team_total["total_matches"],
    )

    plt.title("Partits totals jugats per equip")
    plt.xlabel("Equips")
    plt.ylabel("Nombre total de partits")
    plt.xticks(rotation=90)
    plt.tight_layout()

    plt.savefig(
        f"{config.IMG_PATH}/grafica_ex2_"
        f"{config.nom_alumne}_{config.date_time}.png"
    )
    plt.close()
