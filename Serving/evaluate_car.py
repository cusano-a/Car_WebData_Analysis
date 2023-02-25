import streamlit as st
import pandas as pd
import numpy as np
import os
import datetime

makers_list = ['Fiat', 'Ferrari']
models_list = ['Panda', '458 Italia']
body_types_list = ['Suv', 'Berlina', 'Cabriolet']
fuel_types_list = ['Benzina', 'Diesel', 'Metano', 'GPL', 'Ibrida', 'Elettrica']
gear_list = ['Manuale', 'Automatico', 'Semiautomatico']



st.title('Used Cars Price Evaluator 💵')

st.markdown(
    """
    Evaluate the market price of your car filling the form below 👇
    \n
    \n
"""
)


#Maker and model details
st.selectbox('Maker', 
             options=makers_list,
)

st.selectbox('Model', 
             options=models_list, 
)


#Age status of car details
st.date_input('Registration Date', 
                min_value=datetime.date(1980, 1, 1), 
                max_value=datetime.date.today(),
                help='The first date when the car was registerd'
)

st.number_input('Mileage (Km)',
                value=40000, 
                min_value=0, 
                max_value=1000000, 
                step=10000, 
                format='%i', 
)

#Body details
st.selectbox('Body Type', 
             options=body_types_list, 
)

#Engine Details
st.number_input('Power (CV)',
                value=100,
                min_value=0, 
                max_value=2000, 
                step=10, 
                format='%i', 
)

st.number_input(r'Engine size (cm$^3$)',
                value=1500, 
                min_value=0, 
                max_value=10000, 
                step=100, 
                format='%i', 
)


st.selectbox('Fuel Type', 
             options=fuel_types_list, 
)

st.selectbox('Gear Type', 
             options=gear_list, 
)

st.button('Submit')