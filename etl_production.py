# ---------------------------------------------------------------------------------------
# Cet ETL récupère les données de production éolienne et solaire en France
# sur la période de 2014 à 2025.
#
# Les données sont nettoyées, transformées et enrichies afin de calculer les
# variables nécessaires à l'analyse énergétique et aux modèles de prédiction
# de production.
#
# Le jeu de données finalisé est ensuite fusionné avec le fichier
# "vent_mensuelle_france.csv" et enregistré dans le dossier :
# "data/traites/"
#
# -----------------------------------------------------------------------------------------

import pandas as pd
import pandas as pd

# Charger le fichier

df = pd.read_csv(
    "./data/energies/production-regionale-mensuelle-filiere.csv",
    sep=";",
    encoding="utf-8-sig",
)


# ---------------------------------------------------------------------------------------
# Extraction de l'année et du mois à partir de la colonne date
# afin de faciliter les analyses temporelles.
# ---------------------------------------------------------------------------------------


df[["year", "month"]] = df["Mois"].str.split("-", expand=True)

df = df[
    ["month", "year", "Région", "Production éolienne (GWh)", "Production solaire (GWh)"]
]


# ---------------------------------------------------------------------------------
# Calculer les productions (eoliennes et solaires )  mensuelle par region
# ---------------------------------------------------------------------------------

df = (
    df.groupby(["Région", "year", "month"])
    .agg(
        production_mensuelle_eolienne=("Production éolienne (GWh)", "sum"),
        production_mensuelle_solaire=("Production solaire (GWh)", "sum"),
    )
    .reset_index()
)

df["production_mensuelle_eolienne"] = df["production_mensuelle_eolienne"].round(2)
df["production_mensuelle_solaire"] = df["production_mensuelle_solaire"].round(2)


# Renommer la colonne "Région" par "region"
df = df.rename(columns={"Région": "region"})


df_vent_mensuelle_france = pd.read_csv(
    "./data/traites/vent_mensuelle_france.csv", sep=",", encoding="utf-8-sig"
)


# ---------------------------------------------------------------------------------
# Fusionner avec les données vent mensuelle france
# region,month,year,temp_moy_mensuelle,vent_moy_mensuelle,rayonnement_mensuel
# ---------------------------------------------------------------------------------

df["year"] = df["year"].astype(int)
df["month"] = df["month"].astype(int)

df_vent_mensuelle_france = df_vent_mensuelle_france.merge(
    df, on=["region", "year", "month"], how="left"
)
df_vent_mensuelle_france = df_vent_mensuelle_france.sort_values(
    ["region", "year", "month"]
)
df_vent_mensuelle_france.to_csv("./data/traites/vent_mensuelle_france.csv", index=False)
