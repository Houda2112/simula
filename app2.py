import numpy as np
import pickle
import streamlit as st
import xgboost as xgb


# loading the saved model
loaded_model = pickle.load(open("model.sav", 'rb'))


# creating a function for Prediction

def prediction(input_data):
    # Assurez-vous que votre input_data est une liste ou un tableau NumPy avec les trois features
    input_data_as_numpy_array = np.asarray(input_data)

    # Reshape le tableau si nécessaire
    input_data_reshaped = input_data_as_numpy_array.reshape(1, -1)

    # Faire la prédiction
    prediction = loaded_model.predict(xgb.DMatrix(input_data_reshaped))

    # Afficher la prédiction (remplacez cela par la logique spécifique à votre application)
    print("Prédiction (poids, volume, prix) :", prediction)

    return prediction
  
# Correspondance entre les noms de ville et les codes
city_mapping = {'Berrechid': 0, 'Casablanca': 1, 'El jadida': 2, 'Fes': 3, 'Kenitra': 4, 'Meknes': 5, 'Rabat': 6, 'Tanger': 7}
# Inversion du dictionnaire pour obtenir la correspondance inverse
reverse_city_mapping = {v: k for k, v in city_mapping.items()}
  
def main():
    
    
    # giving a title
    st.title(' Return Scenario')
    
    
    # getting the input data from the user
    
    
    # Obtenir les données d'entrée de l'utilisateur
    Departure = st.selectbox('Departure', list(city_mapping.keys()))
    Arrival = st.selectbox('Arrival', list(city_mapping.keys()))
    TruckType = st.text_input('TruckType')
    
   # Champs de date de départ
    st.write("Departure Date:")
    departure_day = st.selectbox("Departure Day", list(range(1, 32)))
    departure_month = st.selectbox("Departure Month", list(range(1, 13)))
    departure_year = st.selectbox("Departure Year", list(range(2022, 2030)))

    DepartureDate = f"{departure_day}-{departure_month}-{departure_year}"

    # Champs de date d'arrivée
    st.write("Arrival Date:")
    arrival_day = st.selectbox("Arrival Day", list(range(1, 32)))
    arrival_month = st.selectbox("Arrival Month", list(range(1, 13)))
    arrival_year = st.selectbox("Arrival Year", list(range(2022, 2030)))

    ArrivalDate = f"{arrival_day}-{arrival_month}-{arrival_year}"

    # Afficher les données
    st.write("Departure:", Departure)
    st.write("Arrival:", Arrival)
    st.write("TruckType:", TruckType)
    st.write("Departure Date:", DepartureDate)
    st.write("Arrival Date:", ArrivalDate)
    
    
    # Convertir les noms de ville sélectionnés en codes pour l'utilisation du modèle
    departure_code = city_mapping[Departure]
    arrival_code = city_mapping[Arrival]

    
    # code for Prediction
    diagnosis = ''
    
    # creating a button for Prediction
    
    if st.button('Return Scenario'):
        diagnosis = prediction([ departure_code, arrival_code, TruckType, DepartureDate, ArrivalDate ])
        
        
    st.success(diagnosis)
    
    
    
    
    
if __name__ == '__main__':
    main()
    
