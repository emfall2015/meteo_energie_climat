from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import pandas as pd
import joblib
import os
from sklearn.preprocessing import LabelEncoder


#---------------------------------------------------------------------------------------
# Prédire la production éolienne en Bretagne en fonction du vent
# Entraînement jusqu'à 2023 et test sur 2024
#---------------------------------------------------------------------------------------


# Charger les données
df = pd.read_csv(
    "./data/traites/vent_mensuelle_france.csv",
    sep=",",
    encoding="utf-8-sig"
)
df["puissance_installee_eolienne_GW"] = (
    df["puissance_installee_eolienne_MW"] / 1000
)

# encodage des noms des régions 

encoder = LabelEncoder()
df["region_code"] = encoder.fit_transform(df["region"])


#---------------------------------------------------------------------------------------
# Séparer les données entraînement et test
#---------------------------------------------------------------------------------------


df_train = df[
    df["year"] <= 2019
].copy()

df_test = df[
    df["year"] > 2019
].copy()


# Supprimer les lignes sans production
df_train = df_train.dropna(
    subset=["production_mensuelle_eolienne"]
)

df_test = df_test.dropna(
    subset=["production_mensuelle_eolienne"]
)


#---------------------------------------------------------------------------------------
# Variables explicatives
#---------------------------------------------------------------------------------------

features = [
   "region_code",
   "vent_moy_mensuelle",
   "puissance_installee_eolienne_MW",
    "month",
    "year"
]



X_train = df_train[features]
y_train = df_train["production_mensuelle_eolienne"]


X_test = df_test[features]
y_test = df_test["production_mensuelle_eolienne"]


#---------------------------------------------------------------------------------------
# Entraîner le modèle
#---------------------------------------------------------------------------------------

model = RandomForestRegressor(
    n_estimators=400,
    random_state=42
)


model.fit(
    X_train,
    y_train
)


#----------------------------------------------------------------------------------------
# Prédiction 2024
#----------------------------------------------------------------------------------------

y_pred = model.predict(X_test)


# Ajouter les résultats
resultats = df_test[
    [   "region",
        "year",
        "month",
        "vent_moy_mensuelle",
        "puissance_installee_eolienne_MW",
        "production_mensuelle_eolienne"
    ]
].copy()


resultats["production_predite_eolienne"] = y_pred


resultats["erreur_GWh"] = (
    resultats["production_predite_eolienne"]
    - resultats["production_mensuelle_eolienne"]
)


print("--------------------------------")
print("Comparaison production réelle / prédite 2024")
print("--------------------------------")



#---------------------------------------------------------------------------------------
# Evaluation
#---------------------------------------------------------------------------------------

mae = mean_absolute_error(
    y_test,
    y_pred
)

r2 = r2_score(
    y_test,
    y_pred
)


print("--------------------------------")
print("Evaluation année 2024")
print("--------------------------------")

print(f"MAE : {mae:.2f} GWh")
print(f"R²  : {r2:.2f}")


#---------------------------------------------------------------------------------------
# Sauvegarder le modèle
#---------------------------------------------------------------------------------------

os.makedirs("modele", exist_ok=True)

joblib.dump(
    {
        "model": model,
        "encoder": encoder
    },
    "./modele/predict_eolienne.pkl"
)