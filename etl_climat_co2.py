# ---------------------------------------------------------------------------------------
#
# Cet ETL collecte les données climatiques ainsi que les concentrations mondiales
# de CO2 de 1958 à 2025.
#
# Les données sont nettoyées, transformées et enrichies afin de calculer les
# variables nécessaires à l'analyse climatique et aux modèles de prédiction.

# Le jeu de données finalisé est ensuite enregistré dans le dossier "traités"
# pour être utilisé dans les étapes d'analyse.
# ---------------------------------------------------------------------------------------

import pandas as pd
import glob
import geopandas as gpd
import pandas as pd

# Charger les dataset du département

files = glob.glob("data/temperatures/*.csv")


df = pd.concat(
    [pd.read_csv(f, sep=";", encoding="utf-8-sig") for f in files], ignore_index=True
)


df["AAAAMMJJ"] = pd.to_datetime(df["AAAAMMJJ"], format="%Y%m%d")

# Trier par station et date
df = df.sort_values(["NUM_POSTE", "AAAAMMJJ"])


# ---------------------------------------------------------------------------------
# Ajouter la région
# ---------------------------------------------------------------------------------

# retrouver les régions à l'aide de latitude et longitude

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

# Renommer la colonne nom par région
stations_region = stations_region.rename(columns={"nom": "region"})


# Fusionner avec dataframe df pour avoir les régions

df = df.merge(stations_region[["NUM_POSTE", "region"]], on="NUM_POSTE", how="left")

# ---------------------------------------------------------------------------------
# Ajouter une colonne YEAR = quatres premiers chiffres de la colonne AAAAMMJJ
# ---------------------------------------------------------------------------------

df["year"] = df["AAAAMMJJ"].astype(str).str[:4]

# ---------------------------------------------------------------------------------
# TM temperature moyenne quotidienne
# Prendre les colonnes Annee et TM
# ----------------------------------------------------------------------------------

df = df[["year", "TM", "region", "FFM"]]


# ---------------------------------------------------------------------------------
# Calculer la température moyenne annuelle (TM) et la force du vent(FFM) par region
# ---------------------------------------------------------------------------------

temperature_france = (
    df.groupby(["region", "year"])
    .agg(
        temp_moy_annuelle=("TM", "mean"),
        vent_moy_annuelle=("FFM", "mean"),
    )
    .reset_index()
)

# Arrondi à deux chiffres aprés la virgule

temperature_france["temp_moy_annuelle"] = temperature_france["temp_moy_annuelle"].round(
    2
)
temperature_france["vent_moy_annuelle"] = temperature_france["vent_moy_annuelle"].round(
    2
)

# Exporter df dans un fichier
temperature_france.to_csv("./data/traites/temperature_france.csv", index=False)

# ---------------------------------------------------------------------------------
# Chargement Fichier Co2 Global
# ---------------------------------------------------------------------------------

df = pd.read_csv("./data/co2/co2_global.csv", sep=",", encoding="utf-8-sig")

# Récupérer l'année et la concentration de co2

df = df[["year", "CO2_ppm"]]

# ---------------------------------------------------------------------------------
# Suppression des doublons
# ---------------------------------------------------------------------------------

df = df.drop_duplicates()

# Exporter dans le dossier traité


# -------------------------------------------------------------------------------------------
# Fusion des fichiers temperature_france.csv et co2_global.csv en utilisant annee comme clé
# -------------------------------------------------------------------------------------------

temperature_france["year"] = temperature_france["year"].astype(int)
df["year"] = df["year"].astype(int)

df_co2_annee_temps_region = temperature_france.merge(df, on="year", how="inner")
# Exporter le résultat dans  dossier traites
df_co2_annee_temps_region.to_csv(
    "./data/traites/co2_annee_temps_region.csv", index=False
)
