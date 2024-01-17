import numpy as np
import pickle
import streamlit as st


# loading the saved model
loaded_model = pickle.load(open("model.sav", 'rb'))


# creating a function for Prediction

def diabetes_prediction(input_data):
    

    # changing the input_data to numpy array
    input_data_as_numpy_array = np.asarray(input_data)

    # reshape the array as we are predicting for one instance
    input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)

    prediction = loaded_model.predict(input_data_reshaped)
    print(prediction)

    if (prediction[0] == 0):
      return model
  
    
  
def main():
    
    
    # giving a title
    st.title(' Prediction Web Application')
    
    
    # getting the input data from the user
    
    
    origine = st.text_input('origine')
    destination = st.text_input('destination')
    arrivaltime = st.text_input('arrivaltime')
    departuretime = st.text_input('departuretime')
    trucktype = st.text_input('trucktype')
    
    
    
    

    
    # code for Prediction
    diagnosis = ''
    
    # creating a button for Prediction
    
    if st.button('Diabetes Test Result'):
        diagnosis = diabetes_prediction([origine, destination, arrivaltime, departuretime, trucktype ])
        
        
    st.success(diagnosis)
    
    
    
    
    
if __name__ == '__main__':
    main()
    
