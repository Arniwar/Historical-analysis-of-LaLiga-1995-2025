"""Exercici 6: resum estadístic 1995-2025 i capacitat dels estadis."""

import pandas as pd


def fun_total_goals(data: pd.DataFrame) -> tuple[int, int, int]:
    """
    Calcula els gols locals, visitants i totals.

    Args:
        data: DataFrame amb les dades dels partits.

    Returns:
        tuple[int, int, int]: Gols locals, gols visitants i gols totals.
    """
    home_goals = int(data["FTHG"].sum())
    away_goals = int(data["FTAG"].sum())
    total_goals = home_goals + away_goals

    return home_goals, away_goals, total_goals


def fun_total_goals_by_team(
    data: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Calcula els gols locals, visitants i totals per cada equip.

    Args:
        data: DataFrame amb les dades dels partits.

    Returns:
        tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]: DataFrames amb gols
        locals, visitants i totals per equip.
    """
    home_goals_by_team = (
        data.groupby("HomeTeam")["FTHG"].sum().astype(int).reset_index()
    )
    home_goals_by_team.columns = ["team", "home_goals"]

    away_goals_by_team = (
        data.groupby("AwayTeam")["FTAG"].sum().astype(int).reset_index()
    )
    away_goals_by_team.columns = ["team", "away_goals"]

    home_goals_series = home_goals_by_team.set_index("team")["home_goals"]
    away_goals_series = away_goals_by_team.set_index("team")["away_goals"]

    total_goals_by_team = (
        home_goals_series.add(away_goals_series, fill_value=0)
        .astype(int)
        .sort_values(ascending=False)
        .reset_index()
    )
    total_goals_by_team.columns = ["team", "total_goals"]

    return home_goals_by_team, away_goals_by_team, total_goals_by_team


def fun_resum_1996_2025(
    total_points_by_team: pd.Series,
    home_goals_by_team: pd.DataFrame,
    away_goals_by_team: pd.DataFrame,
    total_goals_by_team: pd.DataFrame,
) -> pd.DataFrame:
    """
    Crea el dataframe resum amb punts i gols acumulats per equip.

    Args:
        total_points_by_team: Series amb els punts totals per equip.
        home_goals_by_team: DataFrame amb els gols locals per equip.
        away_goals_by_team: DataFrame amb els gols visitants per equip.
        total_goals_by_team: DataFrame amb els gols totals per equip.

    Returns:
        pd.DataFrame: DataFrame resum amb punts i gols per equip.
    """
    points_df = total_points_by_team.reset_index()
    points_df.columns = ["team", "points"]

    resum_1996_2025 = (
        points_df.merge(home_goals_by_team, on="team", how="outer")
        .merge(away_goals_by_team, on="team", how="outer")
        .merge(total_goals_by_team, on="team", how="outer")
    )

    resum_1996_2025 = resum_1996_2025.fillna(0)

    numeric_columns = ["points", "home_goals", "away_goals", "total_goals"]
    resum_1996_2025[numeric_columns] = resum_1996_2025[numeric_columns].astype(int)

    resum_1996_2025 = resum_1996_2025.sort_values(
        by="points",
        ascending=False,
    ).reset_index(drop=True)

    return resum_1996_2025


def add_stadium_capacity(
    resum_1996_2025: pd.DataFrame,
    stadium_capacity: dict[str, int],
) -> pd.DataFrame:
    """
    Afegeix la capacitat de l'estadi de cada equip al dataframe resum.

    Args:
        resum_1996_2025: DataFrame resum amb estadístiques per equip.
        stadium_capacity: Diccionari amb la capacitat de l'estadi de cada equip.

    Returns:
        pd.DataFrame: DataFrame resum amb la columna stadium_capacity.
    """
    resum_1996_2025 = resum_1996_2025.copy()

    resum_1996_2025["stadium_capacity"] = resum_1996_2025["team"].map(
        stadium_capacity
    )

    return resum_1996_2025