# ---------------------------------------------------------------------------------------
# Cet ETL collecte les données de rayonnemeent solaire mensuelle en France
# sur la période de 1950 à 2024.
#
# Les données sont nettoyées, transformées et enrichies afin de calculer les
# variables nécessaires à l'analyse climatique et aux modèles de prédiction.
#
# Le jeu de données finalisé est ensuite fusionné avec le fichier vent_mensuelle_france dans le dossier :
# "data/traites/"
# ---------------------------------------------------------------------------------------

import pandas as pd
import glob
import geopandas as gpd
import pandas as pd

files = glob.glob("data/ensolleilement/*.csv")

df = pd.concat(
    [pd.read_csv(f, sep=";", encoding="utf-8-sig") for f in files], ignore_index=True
)


df["AAAAMMJJ"] = pd.to_datetime(df["AAAAMMJJ"], format="%Y%m%d")

# Trier par station et date
df = df.sort_values(["NUM_POSTE", "AAAAMMJJ"])


# ---------------------------------------------------------------------------------
# Ajouter la région
# ---------------------------------------------------------------------------------
# retrouver les régions à l'aide de lat et long
# Garder une seule ligne par station
stations = df[["NUM_POSTE", "NOM_USUEL", "LAT", "LON", "ALTI"]].drop_duplicates(
    "NUM_POSTE"
)


# Charger les régions
regions = gpd.read_file("regions.geojson")


# Transformer les stations en points GPS
stations = gpd.GeoDataFrame(
    stations,
    geometry=gpd.points_from_xy(stations["LON"], stations["LAT"]),
    crs="EPSG:4326",
)


# Trouver la région
stations = gpd.sjoin(stations, regions, predicate="within")


# Garder uniquement les informations utiles
stations_region = stations[["NUM_POSTE", "NOM_USUEL", "LAT", "LON", "nom"]]

# Renommer la colonne région
stations_region = stations_region.rename(columns={"nom": "region"})


df = df.merge(stations_region[["NUM_POSTE", "region"]], on="NUM_POSTE", how="left")


# ---------------------------------------------------------------------------------
# prendre les quatres premiers chiffres qui correspond à l'annee
# Ajouter une colonne YEAR
# ---------------------------------------------------------------------------------

df["AAAAMMJJ"] = pd.to_datetime(df["AAAAMMJJ"], format="%Y%m%d", errors="coerce")

df["year"] = df["AAAAMMJJ"].dt.year
df["month"] = df["AAAAMMJJ"].dt.month


df = df[["month", "year", "GLOT", "region"]]


# ---------------------------------------------------------------------------------
# Calculer la rayonnement mensuelle par region
# le champs GLOT correspond au rayonnement global quotidien
# ---------------------------------------------------------------------------------

df_rayonnement_france = (
    df.groupby(["region", "month", "year"])
    .agg(rayonnement_mensuel=("GLOT", "sum"))
    .reset_index()
)


df_vent_france = pd.read_csv(
    "./data/traites/vent_mensuelle_france.csv", sep=",", encoding="utf-8-sig"
)


# -----------------------------------------------------------------------------------
# Fusionner avec les données de la température
# -----------------------------------------------------------------------------------

df_rayonnement_france["year"] = df_rayonnement_france["year"].astype(int)
df_rayonnement_france["month"] = df_rayonnement_france["month"].astype(int)


df_vent_france = df_vent_france.merge(
    df_rayonnement_france, on=["region", "year", "month"], how="left"
)

df_vent_france.to_csv("./data/traites/vent_mensuelle_france.csv", index=False)
