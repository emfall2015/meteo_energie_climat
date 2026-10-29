# Météo - Énergie - Climat


## Présentation du projet

**Météo - Énergie - Climat** est un projet d'analyse et de prédiction autour des données météorologiques, énergétiques et climatiques.

L'objectif est de mettre en pratique les compétences acquises durant la formation en travaillant sur des **datasets réels et volumineux**, en explorant différentes techniques de traitement de données, de visualisation et de modélisation prédictive.

Le projet cherche notamment à répondre aux problématiques suivantes :

> **Analyser l'impact du CO₂ sur le climat en France et prédire les tendances futures.**
> **Prédire la production éolienne et solaire en fonction des conditions météo.**

# Sources des données

Le projet s'appuie notamment sur les jeux de données suivants:

### Production éolienne et solaire

[Parc national annuel de production éolien et solaire — data.gouv.fr](https://www.data.gouv.fr/datasets/parc-national-annuel-de-production-eolien-et-solaire-2001-a-2025)

Ce dataset permet d'étudier l'évolution de la production renouvelable en France sur plusieurs années.

### Production mensuelle

[Courbes de production mensuelles éolien/solaire — data.gouv.fr](https://www.data.gouv.fr/datasets/courbes-de-production-mensuelles-eolien-solaire-complement-de-remuneration)

Ces données permettent notamment d'étudier la saisonnalité de la production.

### Données météorologiques

[Météo-France — données météorologiques](https://meteo.data.gouv.fr/datasets/6569b51ae64326786e4e8e1a)

Les données météorologiques permettent de mettre en relation les conditions météo avec la production énergétique.

### Données climat / CO₂

[Global CO₂ vs Temperature Anomaly Dataset — Kaggle](https://www.kaggle.com/datasets/alitaqishah/global-co-vs-temp-anomaly-dataset-19582025)

# Stack technique


| Technologie          | Utilisation                    |
| -------------------- | ------------------------------ |
| **Python**           | Langage principal              |
| **Pandas**           | Manipulation des données       |
| **Scikit-learn**     | Machine Learning               |
| **Matplotlib**       | Visualisation                  |
| **Seaborn**          | Analyse exploratoire           |
| **Streamlit**        | Exploration et expérimentation |
| **Random Forest**    | Modéle de machine learning     |


# Installation


Cloner le projet :

```bash
git clone https://github.com/emfall2015/meteo_energie_climat.git

```

Lancer les scripts python dans cette ordre : 

```bash
python etl_climat_co2.py
python etl_vent.py
python etl_rayonnement.py
python etl_production.py
python etl_puissance_installee_eolienne.py
```

---

# Préparation des données

Les données passent par plusieurs étapes :

```text
Données brutes dans le dossiers /data
      ↓
Nettoyage
      ↓
Gestion des valeurs manquantes
      ↓
Normalisation des formats
      ↓
Fusion des datasets
      ↓
Feature Engineering
      ↓
Dataset final dans le dossier /traites
      ↓
Machine Learning
```
---

# Lancement de l'application

Depuis la racine du projet :

```bash
streamlit run app/app.py
```

L'application sera ensuite accessible localement à l'adresse indiquée par Streamlit.

---

# Aperçu de l'application

Voici quelques captures d'écran de l'application.

## Page d'accueil

![accueil](./screenshots/accueil1.png)

![accueil](./screenshots/accueil2.png)

![accueil](./screenshots/accueil3.png)

## Evolution de la température et du co2

![temperature_du_co2](./screenshots/.png)

## Enregistrement d'une nouvelle connaissance via le formulaire

![add_connaissance](./screenshots/add_connaissance.png)

## Poser une question 

![poser_question](./screenshots/poser_question.png)

---
