# docker run -it -v "$(pwd):/home/app" -p 4000:4000 jedha/streamlit-fs-image
# docker run -it -v "$(pwd):/home/app" -p 4000:4000 jedha/streamlit-fs-image bash
# docker build . -t NAME_DOCKER
# docker run -it -p 4000:80 -v "$(pwd):/home/app" -e PORT:80 NAME_DOCKER bash

#http://localhost:4000

import streamlit as st
import pandas as pd
import plotly.express as px 
import plotly.graph_objects as go
import requests



DATA_URL = 'https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_delay_analysis.xlsx'

st.set_page_config(layout="wide")
st.markdown(
    """
    <style>
    .main {
        margin: 0 auto; /* Centers the content */
        max-width: 1100px;

    }
    </style>
    """,
    unsafe_allow_html=True
)

@st.cache_data
def load_data(): 
    data = pd.read_excel(DATA_URL)
    return data

data = load_data()
print('state: ',data['state'].value_counts())

st.markdown("""
    <div style="text-align: center;">
        <img src="https://lever-client-logos.s3.amazonaws.com/2bd4cdf9-37f2-497f-9096-c2793296a75f-1568844229943.png" alt="GetAround logo" style="width: 80%;">
    </div>
    
    <br>
    
    Bienvenue sur la page d'accueil du projet `Get Around`. Notre objectif, après analyse de certains paramètres de locations de voiture, est de créer un modèle
            d'apprentissage machine permettant de déterminer le prix optimal pour une location.
    <br><br><br>
""", unsafe_allow_html=True)


st.markdown("""---""")
st.markdown("""<br>""", unsafe_allow_html=True)
st.subheader("1] Exploration des différents types de location")

if st.checkbox('Données brutes'):
    st.subheader('Données brutes')
    st.write(data)
    st.markdown("""
    <div style="background-color: #F5EAF4; padding: 10px;">

    | Nom du champ                                  | Commentaire                                                                                                                  |
    |-----------------------------------------------|------------------------------------------------------------------------------------------------------------------------------|
    | **rental_id**                                 | Identifiant unique de la location                                                                                            |
    | **car_id**                                    | Identifiant unique de la voiture                                                                                             |
    | **checkin_type**                              | Flux utilisé pour l'enregistrement et le retour. (c'est-à-dire accès et retour de la voiture)                                |
    |                                               | - **mobile** : contrat de location signé sur le smartphone du propriétaire                                                   |
    |                                               | - **connect** : voiture équipée de la technologie Connect, ouverte par le conducteur avec son smartphone                     |
    |                                               | *Note : les contrats papier ont été exclus des données car nous n'avons pas de données sur leur retard lors du retour et c'est un cas d'utilisation négligeable* |
    | **state**                                     | annulé signifie que la location n'a pas eu lieu (a été annulée par le conducteur ou le propriétaire).                        |
    | **delay_at_checkout_in_minutes**              | Différence en minutes entre l'heure de fin de location demandée par le conducteur lors de la réservation de la voiture et l'heure réelle à laquelle le conducteur a terminé le retour. Les valeurs négatives signifient que le conducteur a rendu la voiture en avance. |
    | **previous_ended_rental_id**                  | Identifiant de la location précédente terminée de la voiture (NULL lorsqu'il n'y a pas de location précédente ou que le délai avec la location précédente est supérieur à 12 heures). |
    | **time_delta_with_previous_rental_in_minutes**| Différence en minutes entre l'heure de début prévue de cette location et l'heure de fin prévue de la location précédente (lorsque inférieure à 12 heures, NULL si supérieure). |
    
    </div>
    """, unsafe_allow_html=True)



# data = data.drop(['time_delta_with_previous_rental_in_minutes','previous_ended_rental_id'],axis=1)


st.markdown("""
    <br>
    
    Deux types de locations existent : Connect & Mobile.
            
    **Mobile** : le conducteur et le propriétaire se rencontrent et signent tous deux le contrat de location sur le smartphone du propriétaire.
            
    **Connect** : le conducteur ne rencontre pas le propriétaire et ouvre la voiture avec son smartphone.
            
    Répartition des locations selon le type de commande :
""", unsafe_allow_html=True)

fig = px.pie(data, values='car_id', names='checkin_type')
st.plotly_chart(fig)



st.subheader("2] Repartition des locations annulées selon le type de commande")
fig = px.histogram(data, x='checkin_type', color='state')
st.plotly_chart(fig)    


col = 'delay_at_checkout_in_minutes'
col_mean = data[col].mean()
col_std = data[col].std()
# moyenne +/- 2 écarts type
lower_bound = col_mean - 2 * col_std
upper_bound = col_mean + 2 * col_std
print(col_mean,lower_bound,upper_bound)
data = data[(data[col] >= lower_bound) & (data[col] <= upper_bound)]
print('state: ', data['state'].value_counts())


st.subheader("3] Retard des locations")

if st.checkbox('Montrer uniquement les voitures rendues en retard', value=True):
    mini = 0
    df = data[data['delay_at_checkout_in_minutes']>mini]

else:
    df = data
    mini = int(df['delay_at_checkout_in_minutes'].min())

trsh = int(df['delay_at_checkout_in_minutes'].max())
seuil = st.slider("Choisir le temps de retard en minute", mini, int(df['delay_at_checkout_in_minutes'].max()), int(trsh*0.2))
maxi = int(df['delay_at_checkout_in_minutes'].max())

# seuil = st.slider("Choose the minute threshold!", 0, trsh, int(trsh*0.1))

move_upper_mask = df['delay_at_checkout_in_minutes']<seuil
lower_mask = df['delay_at_checkout_in_minutes']>mini
global_mask = move_upper_mask & lower_mask
number_of_rent = len(df[global_mask])
part_of_rent = 100 * len(df[move_upper_mask]) / len(df)

fig_px = px.histogram(df, color='checkin_type', x='delay_at_checkout_in_minutes')
fig = go.Figure(fig_px)

x = seuil

fig.add_shape(
    type="line",
    x0=x, x1=x, y0=0, y1=1,
    line=dict(color="Green", width=2, dash="dash"),
    xref='x', yref='paper'
)

fig.add_shape(
    type="rect",
    x0=mini, x1=x, y0=0, y1=1,
    fillcolor="Green",
    opacity=0.2,
    line_width=0,
    xref='x', yref='paper'
)

fig.update_layout(
    title="",
    xaxis_title="Delay at Checkout in Minutes",
    yaxis_title="Count"
)

fig.add_annotation(
    x=(x+mini)/2,
    y=0.8,    
    xref='x',
    yref='paper',
    text=f"{number_of_rent}",
    showarrow=False,
    font=dict(size=12, color="Green"),
)
fig.add_annotation(
    x=(x+mini)/2,
    y=0.9,    
    xref='x',
    yref='paper',
    text=f"{part_of_rent:.2f}%",
    showarrow=False,
    font=dict(size=16, color="Green"),
)


fig.add_shape(
    type="rect",
    x0=x, x1=maxi, y0=0, y1=1,
    fillcolor="Red",
    opacity=0.2,
    line_width=0,
    xref='x', yref='paper'
)

fig.add_annotation(
    x=(maxi+x)/2,
    y=0.8,    
    xref='x',
    yref='paper',
    text=f"{len(df)-number_of_rent}",
    showarrow=False,
    font=dict(size=12, color="Red"),
)
fig.add_annotation(
    x=(maxi+x)/2,
    y=0.9,    
    xref='x',
    yref='paper',
    text=f"{100-part_of_rent:.2f}%",
    showarrow=False,
    font=dict(size=16, color="Red"),
)


st.plotly_chart(fig)  

st.subheader("4] Impact du retard sur les conducteurs suivant")


df_late_impact = df[df['previous_ended_rental_id'].notna()]

if st.checkbox('Données brutes'):
    st.write(df_late_impact)


fig_px = px.histogram(df_late_impact, color='checkin_type', x='time_delta_with_previous_rental_in_minutes', nbins=35)
fig = go.Figure(fig_px)

fig.update_layout(
    title="",
    xaxis_title="Retard en minutes",
    yaxis_title="Nombre"
)

st.plotly_chart(fig)  

car_brands = ["Citroën", "Peugeot", "PGO", "Renault", "Audi", "BMW", "other", "Mercedes", "Opel", "Volkswagen", "Ferrari", "Maserati", "Mitsubishi", "Nissan", "SEAT", "Subaru", "Toyota"]
fuel_types = ["diesel", "petrol", "hybrid_petrol", "electro"]
paint_colors = ["black", "grey", "white", "red", "silver", "blue", "orange", "beige", "brown", "green"]
car_types = ["convertible", "coupe", "estate", "hatchback", "sedan", "subcompact", "suv", "van"]

st.subheader("5] API de prédiction du prix optimal pour les voitures GetAround")

col1, col2, col3 = st.columns(3)

with col1:
    marque = st.selectbox("Marque", car_brands, index=3)
    kilometrage = st.number_input("Kilométrage", min_value=0, step=1000, value=10000)
    puissance_moteur = st.number_input("Puissance du Moteur (HP)", min_value=0, step=10, value=100)

with col2:
    carburant = st.selectbox("Type de Carburant", fuel_types, index=0)
    couleur_peinture = st.selectbox("Couleur de la Peinture", paint_colors, index=0)
    type_voiture = st.selectbox("Type de Voiture", car_types, index=0)

with col3:
    parking_prive_disponible = st.checkbox("Parking Privé", value=True)
    gps_disponible = st.checkbox("GPS Disponible", value=True)
    climatisation_disponible = st.checkbox("Climatisation", value=True)
    voiture_automatique = st.checkbox("Voiture Automatique", value=False)
    getaround_connect_disponible = st.checkbox("GetAround Connect", value=True)
    regulateur_vitesse_disponible = st.checkbox("Régulateur de Vitesse", value=True)
    pneus_hiver = st.checkbox("Pneus Hiver", value=False)

url = "https://huggingface.co/spaces/deschamps-g/getaroundapi"

if st.button("Prédire le prix optimal de la voiture"):
    input_data = {
        "brand": marque,
        "mileage": kilometrage,
        "engine_power": puissance_moteur,
        "fuel": carburant,
        "paint_color": couleur_peinture,
        "car_type": type_voiture,
        "private_parking_available": parking_prive_disponible,
        "has_gps": gps_disponible,
        "has_air_conditioning": climatisation_disponible,
        "automatic_car": voiture_automatique,
        "has_getaround_connect": getaround_connect_disponible,
        "has_speed_regulator": regulateur_vitesse_disponible,
        "winter_tires": pneus_hiver
    }

    response = requests.post(url, params=input_data)

    if response.status_code == 200:
        result = response.json()
        result = response.json()
        prediction_value = round(result["prediction"], 2)
        st.success(f"Prix de la location {prediction_value} $/jour")
    else:
        st.error(f"Erreur: {response.status_code}")
        st.write(response.text)


st.markdown("""
    <br>
    
    <br>
    
""", unsafe_allow_html=True)