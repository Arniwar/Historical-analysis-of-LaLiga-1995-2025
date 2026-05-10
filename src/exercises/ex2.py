"""Exercici 2: càlcul dels partits totals jugats per equip."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

import config


def total_matches(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula el nombre total de partits jugats per cada equip.

    Es compten els partits jugats com a local i com a visitant.

    Args:
        data: DataFrame amb les dades dels partits.

    Returns:
        pd.DataFrame: DataFrame amb les columnes team i total_matches.
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
    """
    Genera un gràfic de barres amb els partits totals jugats per equip.

    Args:
        matches_team_total: DataFrame amb les columnes team i total_matches.
    """
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