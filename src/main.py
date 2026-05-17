"""
Punt d’entrada de l’EAC6: crido en ordre les funcions dels exercicis 1–7.

He centralitzat el diccionari de capacitats d’estadi aquí per tenir-lo a mà
quan el passo a ``add_stadium_capacity``; les gràfiques i models ja inclouen
el meu nom i la data via ``config`` per identificar les sortides.
"""

from exercises.ex1 import load_and_eda, plot_home_away_goals
from exercises.ex2 import total_matches, plot_matches_team_total
from exercises.ex3 import goal_distribution, plot_goal_ditribution
from exercises.ex4 import FTR, plot_FTR
from exercises.ex5 import add_points, fun_total_points, guanyador_historic
from exercises.ex6 import (
    add_stadium_capacity,
    fun_resum_1996_2025,
    fun_total_goals,
    fun_total_goals_by_team,
)
from exercises.ex7 import assignacio_clusters, model_clusters, plot_clusters

import config


stadium_capacity = {
    "Alaves": 19840,
    "Albacete": 17524,
    "Almeria": 18331,
    "Ath Bilbao": 53331,
    "Ath Madrid": 68456,
    "Barcelona": 99354,
    "Betis": 60270,
    "Cadiz": 21094,
    "Celta": 29000,
    "Compostela": 16666,
    "Cordoba": 20989,
    "Eibar": 8164,
    "Elche": 36017,
    "Espanol": 40500,
    "Extremadura": 11580,
    "Getafe": 17393,
    "Gimnastic": 14600,
    "Girona": 11810,
    "Granada": 19336,
    "Hercules": 29500,
    "Huesca": 9100,
    "La Coruna": 32490,
    "Las Palmas": 32400,
    "Leganes": 12454,
    "Levante": 26354,
    "Logrones": 16000,
    "Malaga": 30044,
    "Mallorca": 23142,
    "Merida": 14600,
    "Murcia": 31179,
    "Numancia": 8261,
    "Osasuna": 23576,
    "Oviedo": 30500,
    "Real Madrid": 81044,
    "Recreativo": 21670,
    "Salamanca": 17341,
    "Santander": 22222,
    "Sevilla": 43883,
    "Sociedad": 39500,
    "Sp Gijon": 29029,
    "Tenerife": 22824,
    "Valencia": 48600,
    "Valladolid": 27618,
    "Vallecano": 14505,
    "Villareal": 22500,
    "Villarreal": 22500,
    "Xerez": 20523,
    "Zaragoza": 20000,
}


def main() -> None:
    """Orquestro tots els passos: EDA, agregacions, punts, resum, clustering i inferència."""

    print("EXERCICI 1")
    data = load_and_eda(config.DATA_PATH)

    print("Primers valors del dataset:")
    print(data.head())

    print("\nÚltims valors del dataset:")
    print(data.tail())

    print("\nInformació general del dataset:")
    data.info()

    print("\nResum estadístic:")
    print(data.describe())

    plot_home_away_goals(data)

    print("\nEXERCICI 2")
    matches_team_total = total_matches(data)
    print(matches_team_total.head(10))

    max_matches = matches_team_total["total_matches"].max()
    # Els que tenen el màxim de partits els interpreto com els que han estat sempre a primera.
    always_first_division = matches_team_total[
        matches_team_total["total_matches"] == max_matches
    ]
    print("\nEquips que sempre han estat a primera divisió:")
    print(always_first_division)

    plot_matches_team_total(matches_team_total)

    print("\nEXERCICI 3")
    distr_gols_locals, distr_gols_visitants = goal_distribution(data)
    print("\nDistribució de gols locals:")
    print(distr_gols_locals)
    print("\nDistribució de gols visitants:")
    print(distr_gols_visitants)

    plot_goal_ditribution(distr_gols_locals, distr_gols_visitants)

    print("\nEXERCICI 4")
    ftr = FTR(data)
    print(ftr)
    plot_FTR(ftr)

    print("\nEXERCICI 5")
    data = add_points(data)
    print(data.head(10))

    total_points_by_team, df_total_points_by_team = fun_total_points(data)
    print(df_total_points_by_team.head(10))

    winner = guanyador_historic(df_total_points_by_team)
    print("\nGuanyador històric:")
    print(winner)

    print("\nEXERCICI 6")
    home_goals, away_goals, total_goals = fun_total_goals(data)
    print(f"Gols locals: {home_goals}")
    print(f"Gols visitants: {away_goals}")
    print(f"Gols totals: {total_goals}")

    home_goals_by_team, away_goals_by_team, total_goals_by_team = (
        fun_total_goals_by_team(data)
    )
    print(total_goals_by_team.head(10))

    resum_1996_2025 = fun_resum_1996_2025(
        total_points_by_team,
        home_goals_by_team,
        away_goals_by_team,
        total_goals_by_team,
    )
    print(resum_1996_2025.head())

    resum_1996_2025 = add_stadium_capacity(
        resum_1996_2025,
        stadium_capacity,
    )
    print(resum_1996_2025.head())

    print("\nEXERCICI 7.1 - Model de 3 clústers")
    # Només filo files amb totes les features numèriques; sense això KMeans rebria NaN.
    resum_model = resum_1996_2025.dropna(
        subset=[
            "points",
            "home_goals",
            "away_goals",
            "total_goals",
            "stadium_capacity",
        ]
    ).copy()

    model_3 = model_clusters(resum_model, 3)
    kmeans_3 = model_3["kmeans"]

    print("Labels del model de 3 clústers:")
    print(kmeans_3.labels_)

    resum_model_3 = assignacio_clusters(resum_model, kmeans_3)
    print(resum_model_3.head())

    plot_clusters(resum_model_3, "total_goals", "points")
    plot_clusters(resum_model_3, "stadium_capacity", "points")

    print("\nEXERCICI 7.2 - Model de 4 clústers")
    model_4 = model_clusters(resum_model, 4)
    kmeans_4 = model_4["kmeans"]

    print("Labels del model de 4 clústers:")
    print(kmeans_4.labels_)

    resum_model_4 = assignacio_clusters(resum_model, kmeans_4)
    print(resum_model_4.head())

    plot_clusters(resum_model_4, "total_goals", "points")
    plot_clusters(resum_model_4, "stadium_capacity", "points")

    # Identifico el clúster amb mitjana de punts més alta i llisto els equips que hi pertanyen.
    cluster_points_mean = (
        resum_model_4.groupby("cluster")["points"]
        .mean()
        .sort_values(ascending=False)
    )
    best_cluster = cluster_points_mean.index[0]

    best_teams = resum_model_4[
        resum_model_4["cluster"] == best_cluster
    ].sort_values(by="points", ascending=False)

    print("\nClúster dels millors equips:")
    print(best_cluster)

    print("\nNombre d'equips en el clúster dels millors:")
    print(len(best_teams))

    print("\nEquips del clúster dels millors:")
    print(best_teams[["team", "points", "cluster"]])

    print("\nEXERCICI 7.3 - Inferència equip Europa")
    # Vector en el mateix ordre que selected_columns a ex7: punts, gols local, visitant, total, aforament.
    new_team_cluster = model_4["kmeans"].predict(
        model_4["scaler"].transform(
            [[1150, 650, 440, 1090, 28000]]
        )
    )

    print(f"L'equip Europa pertany al clúster {new_team_cluster[0]}.")


if __name__ == "__main__":
    main()
