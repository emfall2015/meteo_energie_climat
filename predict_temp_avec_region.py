from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import pandas as pd
import joblib
import os

df = pd.read_csv(
    "./data/traites/co2_annee_temps_region.csv",
    sep=",",
    encoding="utf-8-sig"
)

# Variables explicatives
X = df[["year", "region", "CO2_ppm"]]

# Variable cible
y = df["temp_moy_annuelle"]

# Colonnes
categorical_features = ["region"]
numeric_features = ["year", "CO2_ppm"]

# Transformation de region en variable numerique
preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
        ("num", "passthrough", numeric_features)
    ]
)

# Pipeline
model = Pipeline([
    ("preprocessor", preprocessor),
    ("regressor", RandomForestRegressor(
        n_estimators=200,
        random_state=42
    ))
])

# Séparation apprentissage/test
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Entraînement
model.fit(X_train, y_train)

# Sauvegarde
os.makedirs("modele", exist_ok=True)
joblib.dump(model, "./modele/temp_predictor.pkl")


regions = df["region"].dropna().unique()


X_nouveau = pd.DataFrame({
    "year": [2035] * len(regions),
    "region": regions,
    "CO2_ppm": [1000] * len(regions)
})

predictions = model.predict(X_nouveau)


#-----------------------------------------------------------------------------------------------
rf = model.named_steps["regressor"]
preprocessor = model.named_steps["preprocessor"]

feature_names = preprocessor.get_feature_names_out()

importances = pd.Series(
    rf.feature_importances_,
    index=feature_names
).sort_values(ascending=False)

print(importances)

print(X_train["CO2_ppm"].describe())
#--------------------------------------------------------------------------------


resultats = pd.DataFrame({
    "Région": regions,
    "Température prévue en 2035 avec un taux de 450 Co2": predictions
})
print("#--------------------------------------------------------------------------------------")
print("Prediction en 2035")
print(resultats)


# Récupérer les données réelles de 2024
df_2024 = df[df["year"] == 2024].copy()

# Variables d'entrée
X_2024 = df_2024[["year", "region", "CO2_ppm"]]

# Prédictions
df_2024["temp_predite"] = model.predict(X_2024)

# Comparaison
df_2024["erreur"] = (
    df_2024["temp_predite"] - df_2024["temp_moy_annuelle"]
)
print("#---------------------------------------------------------------------------------------")
print("Comparaison entre les temperatures réelles de 2024 et celles prédites en 2024")
print(df_2024[[
    "region",
    "CO2_ppm",
    "temp_moy_annuelle",
    "temp_predite",
    "erreur"
]])