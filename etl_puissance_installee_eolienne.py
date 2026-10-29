# ---------------------------------------------------------------------------------------
# Cet ETL calcule la puissance installée éolienne (MW) par région, année et mois.
#
# Cette variable sera utilisée comme caractéristique (feature) dans les modèles
# de prédiction de la production d'énergie éolienne future.
#
# ----------------------------------------------------------------------------------------

import pandas as pd

# Charger le dataset

df = pd.read_csv(
    "./data/energies/puissance-d-eolien-installee-region.csv",
    sep=",",
    encoding="utf-8-sig",
)


# Garder la valeur maximal s'il y'a des doublons
df = df.groupby(
    ["date_mesure", "libelle_region", "type_installation", "vecteur"], as_index=False
)["valeur"].max()

# ---------------------------------------------------------------------------------------
# Extraction de l'année et du mois à partir de la colonne date
# afin de faciliter les analyses.
# ---------------------------------------------------------------------------------------


df[["year", "month", "day"]] = df["date_mesure"].str.split("-", expand=True)

df = df[["month", "year", "libelle_region", "valeur"]]

# Renommer la colonne "libelle_region" par "region" et "valeur" par puissance_installee_eolienne_MW
df = df.rename(columns={"libelle_region": "region"})

df = df.rename(columns={"valeur": "puissance_installee_eolienne_MW"})


df["year"] = df["year"].astype(int)
df["month"] = df["month"].astype(int)
df["puissance_installee_eolienne_MW"] = df["puissance_installee_eolienne_MW"].astype(
    float
)


# Faire la somme s'il y'a plusieurs mesures et type d'installation(En mer posé,Terrestre)
df = (
    df.groupby(["region", "year", "month"])["puissance_installee_eolienne_MW"]
    .sum()
    .reset_index()
)


df_vent_mensuelle_france = pd.read_csv(
    "./data/traites/vent_mensuelle_france.csv", sep=",", encoding="utf-8-sig"
)

df_vent_mensuelle_france = df_vent_mensuelle_france.merge(
    df, on=["region", "year", "month"], how="left"
)


df_vent_mensuelle_france = df_vent_mensuelle_france.sort_values(
    ["region", "year", "month"]
)

# Remplacer la colonne puissance_installee_eolienne_MW par la première
# valeur trouvée pour chaque couple région-année, puis à recopier cette valeur sur toutes
# les lignes du même groupe.
# Les mesures sont prises chaque 01-01 de l'année et sont identiques pour toute l'année

df_vent_mensuelle_france["puissance_installee_eolienne_MW"] = (
    df_vent_mensuelle_france.groupby(["region", "year"])[
        "puissance_installee_eolienne_MW"
    ].transform("first")
)


df_vent_mensuelle_france = df_vent_mensuelle_france.sort_values(
    ["region", "year", "month"]
)

df_vent_mensuelle_france.to_csv(
    "./data/traites/vent_mensuelle_france.csv", encoding="utf-8-sig", index=False
)
