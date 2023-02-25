import streamlit as st
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns

st.title('Used Cars in Italy Q4-2022 🚗')

@st.cache_data
def load_data(nrows):
    data = data = pd.read_csv(os.path.join('..', 'data', 'usedcars_dataset.csv'), 
                              nrows=nrows, 
                              sep=";", 
                              usecols=['maker', 'model', 'Anno', 'Chilometraggio', 'potenza_cv', 'Carburante', 'price'])
    data=data.dropna()
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data['anno'] = pd.to_datetime(data['anno'])
    return data

data_load_state = st.text('Loading data...')
data = load_data(1000)
data_load_state.text("Done! (using st.cache_data)")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Number of cars by year')
#hist_values = np.histogram(data['anno'].dt.year, bins=10, range=(1980,2023))[0]
#st.bar_chart(hist_values)
fig, ax = plt.subplots()
sns.histplot(data=data['anno'].dt.year, bins=33, binrange=(1990,2023), ax=ax)
st.pyplot(fig)
