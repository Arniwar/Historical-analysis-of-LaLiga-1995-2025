"""
Exercici 5: punts per partit i classificació acumulada.

Tradueixo ``FTR`` a punts amb dos ``map`` (regles 3-1-0 per local i visitant).
Després agrupo per equip amb ``groupby`` i sumo; combino local i visitant amb
``add`` i ``fill_value=0``. El guanyador històric el obtinc amb ``idxmax`` sobre
la columna de punts.
"""

import pandas as pd


def add_points(data: pd.DataFrame) -> pd.DataFrame:
    """
    Afegeixo ``points_home`` i ``points_away`` segons el resultat.

    Faig ``copy()`` per no mutar el DataFrame original que pugui reutilitzar-se
    des de ``main``.
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
    Sumo punts com a local i com a visitant i retorno Series ordenada i DataFrame.

    La Series la mantinc per reutilitzar-la a l’exercici 6 en el merge del resum.
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
    """Selecciono la fila de l’equip amb màxim ``points``."""
    winner = df_total_points.loc[df_total_points["points"].idxmax()]

    return winner
