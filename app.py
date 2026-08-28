import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import joblib
import numpy as np
from sklearn.metrics import mean_absolute_error, r2_score

# -----------------------------
# CONFIG
# -----------------------------

st.set_page_config(
    page_title="Climat Energie Dashboard",
    page_icon="",
    layout="wide"
)


# -----------------------------
# STYLE
# -----------------------------

st.markdown("""
<style>

.main {
    background-color:#f7f9fc;
}

h1 {
    color:#0b3d91;
}

.card {
    padding:20px;
    border-radius:15px;
    background:white;
    box-shadow:0 4px 15px #ddd;
    text-align:center;
}

</style>
""", unsafe_allow_html=True)



# -----------------------------
# HEADER
# -----------------------------


st.title("Plateforme d'Analyse Climatique et Énergétique")



# -----------------------------
# SIDEBAR
# -----------------------------

menu = st.sidebar.radio(
    "Navigation",
    [
        "Vue générale",
        "CO₂ & Température",
        "Prévision 2035",
        "Régions françaises",
        "Production éolienne",
        "Production solaire"
    ]
)



# -----------------------------
# HOME
# -----------------------------
df_co2_annee_temps_region  = pd.read_csv("./data/traites/co2_annee_temps_region.csv", sep=",", encoding="utf-8-sig")
df_vent_mensuelle_france = pd.read_csv(
    "./data/traites/vent_mensuelle_france.csv",
    sep=",",
    encoding="utf-8-sig"
)
if menu=="Vue générale":

    # ------------------------------------------------------------------
    # DERNIÈRE ANNÉE DISPONIBLE
    # ------------------------------------------------------------------

    derniere_annee = df_co2_annee_temps_region["year"].max()

    df_annee_climat = df_co2_annee_temps_region[
        df_co2_annee_temps_region["year"] == derniere_annee
    ]

    df_annee_vent = df_vent_mensuelle_france[
        df_vent_mensuelle_france["year"] == derniere_annee
    ]


    # ------------------------------------------------------------------
    # INDICATEURS CLIMATIQUES
    # ------------------------------------------------------------------

    temperature_moyenne = df_annee_climat["temp_moy_annuelle"].mean()
    co2_moyen = df_annee_climat["CO2_ppm"].mean()


    # ------------------------------------------------------------------
    # INDICATEURS ÉOLIENS ET SOLAIRES
    # ------------------------------------------------------------------

    vent_moyen = df_annee_vent["vent_moy_mensuelle"].mean()

    # la puissance installée est répétée tous les mois de l'année
    # Prendre que la premiere valeur d'une annee
    
    puissance_eolienne_par_region = (
    df_annee_vent
    .groupby("region")["puissance_installee_eolienne_MW"]
    .first()
    .sort_values(ascending=False)
    )

    puissance_eolienne = puissance_eolienne_par_region.mean()
    
    
    # puissance_eolienne = df_annee_vent[
    #     "puissance_installee_eolienne_MW"
    # ].mean()
    
    
    

    production_eolienne = df_annee_vent[
        "production_mensuelle_eolienne"
    ].mean()

    production_solaire = df_annee_vent[
        "production_mensuelle_solaire"
    ].mean()

    rayonnement_moyen = df_annee_vent[
        "rayonnement_mensuel"
    ].mean()


    # ------------------------------------------------------------------
    # RÉGION AVEC LA PLUS FORTE PRODUCTION ÉOLIENNE
    # ------------------------------------------------------------------

    production_par_region = (
        df_annee_vent
        .groupby("region")["production_mensuelle_eolienne"]
        .mean()
        .sort_values(ascending=False)
    )

    region_eolienne_max = production_par_region.index[0]
    production_region_max = production_par_region.iloc[0]


    # -----------------------------
    # AFFICHAGE DES INDICATEURS
    # -----------------------------

    col1, col2, col3, col4 = st.columns(4)


    with col1:
        st.metric(
            "Température moyenne",
            f"{temperature_moyenne:.1f} °C"
        )


    with col2:
        st.metric(
            "CO₂ atmosphérique",
            f"{co2_moyen:.1f} ppm"
        )


    with col3:
        st.metric(
            "Vent moyen",
            f"{vent_moyen:.1f} m/s"
        )


    with col4:
        st.metric(
            "Puissance éolienne installée",
            f"{puissance_eolienne:.0f} MW"
        )


    col5, col6, col7, col8 = st.columns(4)


    with col5:
        st.metric(
            "Production éolienne moyenne",
            f"{production_eolienne:.1f} GWh"
        )


    with col6:
        st.metric(
            "Production solaire moyenne",
            f"{production_solaire:.1f} GWh"
        )


    with col7:
        st.metric(
            "Rayonnement moyen",
            f"{rayonnement_moyen:.1f} J/cm2"
        )


    with col8:
        st.metric(
            "Région la plus productive en éolien",
            region_eolienne_max,
            f"{production_region_max:.1f} GWh"
        )

    st.divider()

    st.subheader(
        "Évolution du CO2 et de la température en Ile-de-France"  
    )
    
    df_final = (
    df_co2_annee_temps_region[
        df_co2_annee_temps_region["region"] == "Île-de-France"
    ]
    .sort_values("year")
    )

    fig = go.Figure()

    fig.add_trace(
    go.Scatter(
        x=df_final["year"],
        y=df_final["temp_moy_annuelle"],
        name="Température",
        line=dict(color="crimson", width=3),
        yaxis="y1"
    )
    )

    fig.add_trace(
    go.Scatter(
        x=df_final["year"],
        y=df_final["CO2_ppm"],
        name="CO₂",
        line=dict(color="royalblue", width=3),
        yaxis="y2"
    )
)

    fig.update_layout(
    title="Évolution du CO₂ et de la température en Île-de-France",
    hovermode="x unified",
    xaxis=dict(title="Année"),
    
    yaxis=dict(
    title=dict(
        text="Température (°C)",
        font=dict(color="crimson")
    ),
    tickfont=dict(color="crimson"),
),

yaxis2=dict(
    title=dict(
        text="CO₂ (ppm)",
        font=dict(color="royalblue")
    ),
    tickfont=dict(color="royalblue"),
    overlaying="y",
    side="right",
),
    height=600,
)
    fig.update_layout(
    template="plotly_white",
    hovermode="x unified",
    legend=dict(
        orientation="h",
        y=1.08,
        x=0.5,
        xanchor="center"
    ),
    title_x=0.5,
)

    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridcolor="lightgray")

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Production moyenne éolienne et solaire par région")


    df_production_region = (
        df_vent_mensuelle_france
        .groupby("region")[
            [
                "production_mensuelle_eolienne",
                "production_mensuelle_solaire"
            ]
        ]
        .mean()
        .reset_index()
    )


    df_production_region = df_production_region.rename(
        columns={
            "production_mensuelle_eolienne": "Éolien",
            "production_mensuelle_solaire": "Solaire"
        }
    )


    df_production_long = df_production_region.melt(
        id_vars="region",
        value_vars=["Éolien", "Solaire"],
        var_name="Source",
        value_name="Production"
    )


    fig = px.bar(
        df_production_long,
        x="region",
        y="Production",
        color="Source",
        barmode="group",
        title="",
        labels={
            "region": "Région",
            "Production": "Production moyenne (GWh)",
            "Source": "Source d'énergie"
        }
    )


    fig.update_layout(
        height=500,
        xaxis_tickangle=-45
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )

# -----------------------------
# CO2 TEMPERATURE
# -----------------------------

elif menu=="CO₂ & Température":

    st.header(
        "Comment le CO₂ influence-t-il les températures en France ?"
    )

        

        

    # Affichage du tableau
    st.subheader("Données utilisées")
    st.dataframe(df_co2_annee_temps_region, use_container_width=True)



    # Tri des données
    df_final = df_co2_annee_temps_region.sort_values("year")

    # Création de la figure
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # ============================
    # Température (axe de gauche)
    # ============================
    for region in df_final["region"].unique():
        df_region = df_final[df_final["region"] == region]

        ax1.plot(
            df_region["year"],
            df_region["temp_moy_annuelle"],
            linewidth=2,
            label=region
        )

    ax1.set_xlabel("Année")
    ax1.set_ylabel(
        "Température moyenne annuelle (°C)",
        color="tab:red"
    )

    ax1.tick_params(
        axis="y",
        labelcolor="tab:red"
    )

    # Affichage d'une année sur 5 pour éviter la surcharge
    ax1.set_xticks(df_final["year"].unique()[::5])
    plt.setp(ax1.get_xticklabels(), rotation=45)


    # ============================
    # CO2 (axe de droite)
    # ============================
    ax2 = ax1.twinx()

    # Une seule courbe de CO2
    df_co2 = (
        df_final[["year", "CO2_ppm"]]
        .drop_duplicates()
        .sort_values("year")
    )

    ax2.plot(
        df_co2["year"],
        df_co2["CO2_ppm"],
        color="black",
        linestyle="--",
        linewidth=3,
        label="CO₂ (ppm)"
    )

    ax2.set_ylabel(
        "CO₂ (ppm)",
        color="black"
    )

    ax2.tick_params(
        axis="y",
        labelcolor="black"
    )


    # ====================================
    # Légende commune
    # ====================================
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()

    ax1.legend(
        lines1 + lines2,
        labels1 + labels2,
        title="Région / CO₂",
        loc="upper left"
    )


    # ============================
    # Mise en forme
    # ============================
    plt.title(
        "Évolution de la température moyenne annuelle et du CO₂"
    )

    ax1.grid(True)

    plt.tight_layout()


    # ============================
    # Affichage dans Streamlit
    # ============================
    st.pyplot(fig)



    # -----------------------------
    # PREDICTION 2035
    # -----------------------------
elif menu=="Prévision 2035":


        st.header(
                "Prédire la température moyenne en 2035"
                )


        co2 = st.slider(
        "Emission CO₂ future",
                100,
                500,
                450
        )
        
        st.info("lles données d'entraînement couvrent uniquement une plage de" 
                 " 315 à 425 ppm. Les scénarios futurs dépassant cette plage constituent " 
                 "donc une extrapolation, domaine dans lequel le Random Forest est limité." 
                 " Ainsi, les prédictions peuvent rester constantes lorsque le CO2 augmente "
                 " fortement au-delà des valeurs observées historiquement.")

        # Charger le modèle
        model = joblib.load("./modele/temp_predictor.pkl")


        # Récupérer les régions
        regions = df_co2_annee_temps_region["region"].dropna().unique()


        # Données futures
        X_nouveau = pd.DataFrame({
            "year": [2035] * len(regions),
            "region": regions,
            "CO2_ppm": [co2] * len(regions)
        })

        
        # Prédiction pour chaque région
        temperature_predite = model.predict(X_nouveau)


        # ============================
        # Graphique des prédictions
        # ============================

        fig = go.Figure()


        for i, region in enumerate(regions):

            # température prédite pour cette région
            temp_2035 = temperature_predite[i]

            # récupérer la dernière température connue de la région
            df_region = df_co2_annee_temps_region[
                df_co2_annee_temps_region["region"] == region
            ].sort_values("year")


            derniere_temp = df_region["temp_moy_annuelle"].iloc[-1]
            derniere_annee = df_region["year"].iloc[-1]


            # Création d'une évolution vers 2035
            annees = [
                derniere_annee,
                2025,
                2030,
                2035
            ]

            temperatures = [
                derniere_temp,
                derniere_temp + (temp_2035 - derniere_temp) * 0.25,
                derniere_temp + (temp_2035 - derniere_temp) * 0.60,
                temp_2035
            ]


            fig.add_trace(
                go.Scatter(
                    x=annees,
                    y=temperatures,
                    mode="lines+markers",
                    name=region
                )
            )


        # Mise en forme
        fig.update_layout(
            title="Prédiction de la température en 2035 par région (CO₂ = 450 ppm)",
            xaxis_title="Année",
            yaxis_title="Température moyenne annuelle (°C)",
            hovermode="x unified",
            height=600
        )


        st.plotly_chart(fig, use_container_width=True)
        
    
        # Récupérer les données réelles de 2024
        df_2024 = df_co2_annee_temps_region[df_co2_annee_temps_region["year"] == 2024].copy()
        
        X_2024 = df_2024[["year", "region", "CO2_ppm"]]
        
        # Prédictions
        
        df_2024["temp_predite"] = model.predict(X_2024)

        # Comparaison 
        df_2024["erreur"] = (
            df_2024["temp_predite"] - df_2024["temp_moy_annuelle"]
        )

        st.subheader("Comparaison entre températures réelles et prédites en 2024")
        st.markdown(""" Mesure de la précision du modéle""")

        # Sélection des colonnes à afficher
        df_comparaison = df_2024[[
            "region",
            "CO2_ppm",
            "temp_moy_annuelle",
            "temp_predite",
            "erreur"
        ]]

        # Renommer les colonnes pour l'affichage
        df_comparaison = df_comparaison.rename(columns={
            "region": "Région",
            "CO2_ppm": "CO₂ (ppm)",
            "temp_moy_annuelle": "Température réelle (°C)",
            "temp_predite": "Température prédite (°C)",
            "erreur": "Erreur (°C)"
        })

        
        # Affichage tableau interactif
        st.dataframe(
            df_comparaison,
            use_container_width=True
        )



# -----------------------------
# REGIONS
# -----------------------------

elif menu=="Régions françaises":

    st.header(
    "Impact du CO₂ sur la température selon les régions"
    )

    # Calcul de l'impact du CO2 par région
    impact_data = []

    for region in df_co2_annee_temps_region["region"].unique():

        df_region = df_co2_annee_temps_region[
            df_co2_annee_temps_region["region"] == region
        ]


        # température proche de 300 ppm
        temp_300 = df_region.loc[
            (df_region["CO2_ppm"] - 300).abs().idxmin(),
            "temp_moy_annuelle"
        ]


        # température proche de 450 ppm
        temp_450 = df_region.loc[
            (df_region["CO2_ppm"] - 450).abs().idxmin(),
            "temp_moy_annuelle"
        ]


        impact = temp_450 - temp_300


        impact_data.append({
            "Region": region,
            "Impact": round(impact, 2)
        })


    # Création du dataframe final
    data = pd.DataFrame(impact_data)


    # Affichage tableau
    #st.subheader("Impact du CO₂ par région")
    st.markdown("Combien la température moyenne d'une région augmente lorsque le CO2 passe approximativement de 300 ppm à 450 ppm")

    st.dataframe(data)


    # Graphique
    fig = px.bar(
        data,
        x="Region",
        y="Impact",
        color="Region",
        title="Augmentation de température estimée pour une hausse du CO2",
        labels={
            "Region": "Région",
            "Impact": "Augmentation température (°C)"
        }
    )


    fig.update_layout(
        yaxis_title="Impact du CO2 (°C)",
        xaxis_title="Région"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )



# -----------------------------
# WIND
# -----------------------------

elif menu=="Production éolienne":

    st.header(
        "Prédire la production éolienne par région"
    )


    # Slider pour choisir le vent
    vent = st.slider(
        "Vitesse moyenne du vent (m/s)",
        min_value=0.0,
        max_value=20.0,
        value=7.0,
        step=0.1
    )


    # Choix du mois et de l'année
    mois = st.selectbox(
        "Mois de prédiction",
        range(1, 13),
        format_func=lambda x: [
            "Janvier", "Février", "Mars", "Avril",
            "Mai", "Juin", "Juillet", "Août",
            "Septembre", "Octobre", "Novembre", "Décembre"
        ][x-1]
    )

    annee = st.number_input(
        "Année de prédiction",
        min_value=2025,
        max_value=2050,
        value=2025
    )


    # Charger le modèle
    data = joblib.load("./modele/predict_eolienne.pkl")

    model = data["model"]
    encoder = data["encoder"]


    # Régions disponibles
    regions = df_vent_mensuelle_france["region"].unique()


    # Données pour la prédiction
    X_regions = pd.DataFrame({
        "region_code": encoder.transform(regions),
        "vent_moy_mensuelle": [vent] * len(regions),
        "puissance_installee_eolienne_MW": [
            df_vent_mensuelle_france[
                "puissance_installee_eolienne_MW"
            ].mean()
        ] * len(regions),
        "month": [mois] * len(regions),
        "year": [annee] * len(regions)
    })


    # Prédiction
    predictions = model.predict(X_regions)


    # Résultats
    df_predictions = pd.DataFrame({
        "region": regions,
        "production_predite_eolienne": predictions
    })


    st.subheader(
        f"Production prévue avec un vent moyen de {vent} m/s"
    )

    st.dataframe(df_predictions)


    # Graphique
    fig = px.bar(
        df_predictions,
        x="region",
        y="production_predite_eolienne",
        color="region",
        title=f"Production éolienne prédite ({annee})",
        labels={
            "region": "Région",
            "production_predite_eolienne": "Production (GWh)"
        }
    )


    fig.update_layout(
        height=500,
        showlegend=False
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )
    
    ## Test du modéle 
    

    st.header(
        "Évaluation du modèle de prédiction de production éolienne"
    )


    # =============================================================
    # Chargement du modèle
    # =============================================================

    data = joblib.load(
        "./modele/predict_eolienne.pkl"
    )

    model = data["model"]
    encoder = data["encoder"]


    # ==========================================
    # Données de test : 2020 - 2024
    # ==========================================

    df_test = df_vent_mensuelle_france[
        df_vent_mensuelle_france["year"] >= 2020
    ].copy()


    # Supprimer les lignes sans production réelle
    df_test = df_test.dropna(
        subset=[
            "production_mensuelle_eolienne"
        ]
    )


    # Encoder les régions

    df_test["region_code"] = encoder.transform(
        df_test["region"]
    )


    # ==========================================
    # Prédiction du modèle
    # ==========================================

    X_test = df_test[
        [
            "region_code",
            "vent_moy_mensuelle",
            "puissance_installee_eolienne_MW",
            "month",
            "year"
        ]
    ]


    df_test["production_predite_eolienne"] = model.predict(
        X_test
    )


    # Calcul erreur

    df_test["erreur_GWh"] = (
        df_test["production_predite_eolienne"]
        -
        df_test["production_mensuelle_eolienne"]
    )


    # ==========================================
    # Sélection région
    # ==========================================

    region = st.selectbox(
        "Choisir une région",
        sorted(df_test["region"].unique())
    )


    df_region = (
        df_test[
            df_test["region"] == region
        ]
        .sort_values(
            ["year", "month"]
        )
    )


    # Création date pour graphique

    df_region["date"] = pd.to_datetime(
        df_region["year"].astype(str)
        +
        "-"
        +
        df_region["month"].astype(str)
        +
        "-01"
    )


    # ==========================================
    # Indicateurs du modèle
    # ==========================================

    mae = mean_absolute_error(
        df_region["production_mensuelle_eolienne"],
        df_region["production_predite_eolienne"]
    )


    r2 = r2_score(
        df_region["production_mensuelle_eolienne"],
        df_region["production_predite_eolienne"]
    )


    col1, col2 = st.columns(2)


    col1.metric(
        "MAE",
        f"{mae:.2f} GWh"
    )


    col2.metric(
        "R²",
        f"{r2:.2f}"
    )


    # ==========================================
    # Graphique réel vs prédit
    # ==========================================

    st.subheader(
        f"Production réelle vs prédite - {region} (2020-2024)"
    )


    fig = go.Figure()


    fig.add_trace(
        go.Scatter(
            x=df_region["date"],
            y=df_region["production_mensuelle_eolienne"],
            mode="lines+markers",
            name="Production réelle"
        )
    )


    fig.add_trace(
        go.Scatter(
            x=df_region["date"],
            y=df_region["production_predite_eolienne"],
            mode="lines+markers",
            name="Production prédite",
            line=dict(
                dash="dash"
            )
        )
    )


    fig.update_layout(
        title=f"Comparaison production éolienne - {region}",
        xaxis_title="Date",
        yaxis_title="Production (GWh)",
        hovermode="x unified",
        height=550
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )



    # les données Avant / jusqu'à 2019
    df_inf = (
                df_vent_mensuelle_france[
                    df_vent_mensuelle_france["year"] <= 2019
                ]
                .groupby("region")["production_mensuelle_eolienne"]
                .mean()
            )

    # les données Après 2019
    df_sup = (
                df_vent_mensuelle_france[
                    df_vent_mensuelle_france["year"] > 2019
                ]
                .groupby("region")["production_mensuelle_eolienne"]
                .mean()
            )

    # Tableau comparatif
    comparaison = pd.DataFrame({
                "Avant_2019": df_inf,
                "Apres_2019": df_sup
            })

    #************************************
            
        

    comparaison = (
        df_vent_mensuelle_france
        .assign(
            periode=lambda x: np.where(
                x["year"] < 2020,
                "Avant_2019",
                "Apres_2019"
            )
        )
        .groupby(["region", "periode"])["production_mensuelle_eolienne"]
        .mean()
        .unstack()
        .reset_index()
    )

    
    st.write(comparaison)
    
    # st.warning("le Random forest sous estime les régions ou la production a fortement évolué aprés 2020.") 
    st.warning(
    "Conclusion : "
    "la production éolienne augmente après 2020, "
    "mais cette évolution varie selon les régions. Le Random Forest, "
    "entrainé sur les données avant 2020, peut étre moins performant "
    "lorsque les niveaux de production après 2020 s'éloignent fortement "
    "de ceux observés pendant l'entrainement. Cette différence de "
    "distribution entre les périodes peut expliquer une partie des "
    "erreurs de prédiction"
    )
# -----------------------------
# SOLAR
# -----------------------------

elif menu=="Production solaire":

        # Choix de la région
    region = st.selectbox(
        "Choisir une région",
        sorted(df_vent_mensuelle_france["region"].unique())
    )


    # Choix de l'année
    
    annee = st.selectbox(
    "Choisir une année",
    sorted(
        df_vent_mensuelle_france[
            df_vent_mensuelle_france["year"] > 2013
        ]["year"].unique()
    )
    )


    # Filtrer région + année
    df_region = df_vent_mensuelle_france[
        (df_vent_mensuelle_france["region"] == region)
        &
        (df_vent_mensuelle_france["year"] == annee)
    ].copy()


    # Garder seulement les données solaires disponibles
    df_region = df_region.dropna(
        subset=[
            "production_mensuelle_solaire"
        ]
    )


    # Trier par mois
    df_region = df_region.sort_values(
        "month"
    )


    # ==========================
    # Graphique deux axes
    # ==========================

    fig = go.Figure()


    # Production solaire
    fig.add_trace(
        go.Scatter(
            x=df_region["month"],
            y=df_region["production_mensuelle_solaire"],
            mode="lines+markers",
            name="Production solaire (GWh)",
            yaxis="y1"
        )
    )


    # Rayonnement
    fig.add_trace(
        go.Scatter(
            x=df_region["month"],
            y=df_region["rayonnement_mensuel"],
            mode="lines+markers",
            name="Rayonnement mensuel",
            yaxis="y2"
        )
    )


    fig.update_layout(

        title=f"Impact du rayonnement sur la production solaire - {region} ({annee})",

        xaxis=dict(
            title="Mois",
            tickmode="array",
            tickvals=list(range(1,13)),
            ticktext=[
                "Jan",
                "Fév",
                "Mar",
                "Avr",
                "Mai",
                "Juin",
                "Juil",
                "Août",
                "Sep",
                "Oct",
                "Nov",
                "Déc"
            ]
        ),


        # Axe gauche
        yaxis=dict(
            title="Production solaire (GWh)"
        ),


        # Axe droit
        yaxis2=dict(
            title="Rayonnement mensuel",
            overlaying="y",
            side="right"
        ),


        hovermode="x unified",
        height=550
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )
    

# -------------------------------------------------------------------------------------
# CORRELATIONS
# -------------------------------------------------------------------------------------

