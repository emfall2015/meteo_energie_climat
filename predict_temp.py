#---------------------------------------------------------------------------------------
# Prédire la température moyenne en 2035 en fonction des émissions de CO2
#---------------------------------------------------------------------------------------

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import pandas as pd
import joblib
import os


df = pd.read_csv("./data/traites/co2_annee_temps_region.csv",sep=",", encoding="utf-8-sig")


# Features (X) et cible (y)
X = df[["year", "CO2_ppm"]]
y = df["temp_moy_annuelle"]

#---------------------------------------------------------------------------------------
# Apprentissage Test 
#---------------------------------------------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

#---------------------------------------------------------------------------------------
# Entrainement
#---------------------------------------------------------------------------------------

model = RandomForestRegressor().fit(X_train, y_train)

#---------------------------------------------------------------------------------------
# Sauvegarder le modèle
# Créer le dossier s'il n'existe pas
#---------------------------------------------------------------------------------------

os.makedirs("modele", exist_ok=True)
joblib.dump(model, "./modele/temp_predictor.pkl")


#---------------------------------------------------------------------------------------
# Charger le modèle entrainé
#---------------------------------------------------------------------------------------

model = joblib.load("./modele/temp_predictor.pkl")

#---------------------------------------------------------------------------------------
# Nouvelle valeur de CO2 
#---------------------------------------------------------------------------------------

co2 = 450

X_nouveau = pd.DataFrame({
     "year":[2035],
      "CO2_ppm": [co2]
   
})

# Faire la prédiction
temperature_predite = model.predict(X_nouveau)

print("CO2 :", co2)
print("Température moyenne annuelle prévue en 2035:", temperature_predite[0])

