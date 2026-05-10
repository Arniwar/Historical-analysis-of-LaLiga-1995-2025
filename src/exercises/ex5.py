"""Exercici 5: classificació global acumulada 1995-2025."""

import pandas as pd


def add_points(data: pd.DataFrame) -> pd.DataFrame:
    """
    Afegeix els punts aconseguits per l'equip local i visitant en cada partit.

    Args:
        data: DataFrame amb les dades dels partits.

    Returns:
        pd.DataFrame: DataFrame amb les columnes points_home i points_away.
    """
    data = data.copy()

    data["points_home"] = data["FTR"].map(
        {
            "H": 3,
            "D": 1,
            "A": 0,
        }
    )

    data["points_away"] = data["FTR"].map(
        {
            "H": 0,
            "D": 1,
            "A": 3,
        }
    )

    return data


def fun_total_points(data: pd.DataFrame) -> tuple[pd.Series, pd.DataFrame]:
    """
    Calcula els punts totals acumulats per cada equip.

    Args:
        data: DataFrame amb les columnes points_home i points_away.

    Returns:
        tuple[pd.Series, pd.DataFrame]: Series i DataFrame amb els punts totals.
    """
    home_points = data.groupby("HomeTeam")["points_home"].sum()
    away_points = data.groupby("AwayTeam")["points_away"].sum()

    total_points_by_team = (
        home_points.add(away_points, fill_value=0)
        .astype(int)
        .sort_values(ascending=False)
    )

    df_total_points_by_team = total_points_by_team.reset_index()
    df_total_points_by_team.columns = ["team", "points"]

    return total_points_by_team, df_total_points_by_team


def guanyador_historic(df_total_points: pd.DataFrame) -> pd.Series:
    """
    Retorna l'equip amb més punts acumulats.

    Args:
        df_total_points: DataFrame amb les columnes team i points.

    Returns:
        pd.Series: Fila corresponent a l'equip amb més punts.
    """
    winner = df_total_points.loc[df_total_points["points"].idxmax()]

    return winner