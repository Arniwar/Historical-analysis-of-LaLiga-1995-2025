"""
Exercici 6: gols totals, gols per equip i taula resum amb merge.

Per als gols globals sumo ``FTHG`` i ``FTAG``. Per equip faig ``groupby`` per
local i visitant i després combino amb ``add`` i ``fill_value=0``. El resum el
construeixo amb ``merge`` successius (outer) per incloure tots els equips que
apareguin en qualsevol taula; omplo NaN amb 0 i converteixo a enters. La
capacitat de l’estadi la uneixo amb ``map`` des del diccionari que defineixo a
``main``.
"""

import pandas as pd


def fun_total_goals(data: pd.DataFrame) -> tuple[int, int, int]:
    """Sumo tots els gols locals, tots els visitants i en faig la suma global."""
    home_goals = int(data["FTHG"].sum())
    away_goals = int(data["FTAG"].sum())
    total_goals = home_goals + away_goals

    return home_goals, away_goals, total_goals


def fun_total_goals_by_team(
    data: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Calculo gols marcats com a local, encaixats com a visitant i total per equip.

    Passo per Series indexades per ``team`` per alinear correctament abans de
    sumar local + visitant.
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
    Uneixo punts i les tres mètriques de gols en un sol DataFrame per equip.

    Utilitzo ``how='outer'`` per no perdre equips amb dades només en una de les
    taules; després normalitzo tipus i ordeno per punts.
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
    Afegeixo ``stadium_capacity`` alineant per nom d’equip.

    Els equips sense entrada al diccionari queden amb NaN a aquesta columna;
    més endavant, a l’exercici 7, faig ``dropna`` abans del clustering.
    """
    resum_1996_2025 = resum_1996_2025.copy()

    resum_1996_2025["stadium_capacity"] = resum_1996_2025["team"].map(
        stadium_capacity
    )

    return resum_1996_2025
