# -*- coding: utf-8 -*-
"""Untitled12.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1f_S17LFPPx2CGg1W_h-PlnpNmKANMj4m
"""

#pip install streamlit

import streamlit as st
import joblib
import pandas as pd
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Charger les données
file_path = "data.csv"
data = pd.read_csv(file_path, error_bad_lines=False)

df_encoded = pd.get_dummies(data, columns=['Origine', 'Destination'])

# Convertir les colonnes de temps en format datetime
df_encoded ['DepartureTime'] = pd.to_datetime(df_encoded ['DepartureTime'])
df_encoded ['ArrivalTime'] = pd.to_datetime(df_encoded ['ArrivalTime'])

# Séparer les colonnes en jour, mois, année et heure pour DepartureTime
df_encoded ['DepartureYear'] = df_encoded ['DepartureTime'].dt.year
df_encoded ['DepartureMonth'] = df_encoded ['DepartureTime'].dt.month
df_encoded ['DepartureDay'] = df_encoded ['DepartureTime'].dt.day
df_encoded ['DepartureHour'] = df_encoded ['DepartureTime'].dt.hour

# Séparer les colonnes en jour, mois, année et heure pour ArrivalTime
df_encoded ['ArrivalYear'] = df_encoded ['ArrivalTime'].dt.year
df_encoded ['ArrivalMonth'] = df_encoded ['ArrivalTime'].dt.month
df_encoded ['ArrivalDay'] = df_encoded ['ArrivalTime'].dt.day
df_encoded ['ArrivalHour'] = df_encoded ['ArrivalTime'].dt.hour

# Supprimer les colonnes originales de temps si nécessaire
df_encoded  = df_encoded .drop(['DepartureTime', 'ArrivalTime'], axis=1)

# Afficher le DataFrame mis à jour
print(df_encoded )

colonnes_drop = ['Weight_ratio', 'Volume_ratio', 'Weight_dispo', 'Volume_dispo', 'FreightType','TruckID','New_Cost', 'distance','Consumption','CO2_EMISSION_ENg' ]
df_encoded = df_encoded.drop(colonnes_drop, axis=1)

nv = [
    col for col in df_encoded.columns if col not in ['Weight', 'Volume', 'Price']
] + ['Weight', 'Volume', 'Price']

# Réorganiser les colonnes
df_encoded = df_encoded[nv]

# Séparer les features (X) et les cibles (y)
X = df_encoded.drop(['Weight', 'Volume', 'Price'], axis=1)
y =  df_encoded[['Weight', 'Volume', 'Price']]

# Séparation des données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entraînement du modèle XGBoost
xgb_model = XGBRegressor(objective='reg:squarederror', random_state=42)
xgb_model.fit(X_train, y_train)

# Évaluation du modèle sur les données de test
y_pred = xgb_model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
st.write(f'Mean Squared Error on Test Data: {mse}')

!pip install pyngrok

!nohup streamlit run your_app.py &

from pyngrok import ngrok

# Set the authtoken
ngrok.set_auth_token('2b3fo39429SNdfOTGxaIJykzJi3_6M5Gzit4ZF15vyuVsRkLe')

# Create ngrok tunnel
public_url = ngrok.connect(8501)

# Display the link to access the app
print('Streamlit app is live at:', public_url)

!streamlit run /usr/local/lib/python3.10/dist-packages/colab_kernel_launcher.py

# Enregistrez le modèle après l'entraînement
joblib.dump(xgb_model, 'modele.pkl')

# Fonction pour prédire avec le modèle
def predict(features):
    features = pd.DataFrame(features, columns=X.columns)
    prediction = xgb_model.predict(features)
    return prediction

## Interface utilisateur Streamlit
def main():
    st.title('Prédiction et Analyse What-If')

    # Ajoutez des composants d'interface utilisateur pour les fonctionnalités nécessaires
    volumes = st.slider('Volumes', 0, 100, 50)
    poids = st.slider('Poids', 0, 1000, 500)
    ville_depart = st.selectbox('Ville de départ', ['Casablanca', 'Autre'])
    ville_arrivee = st.selectbox('Ville d\'arrivée', ['Marrakech', 'Autre'])
    villes_passage = st.multiselect('Villes de passage', ['Rabat', 'Fes', 'Autre'])

    if st.button('Prédire'):
        prediction = predict(volumes, poids, ville_depart, ville_arrivee, villes_passage)
        st.success(f'La prédiction est : {prediction}')

    # Ajoutez des composants d'interface utilisateur pour l'analyse what-if

if __name__ == '__main__':
    main()

