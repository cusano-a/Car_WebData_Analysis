import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from serving_helpers import load_data

st.title("Used Cars in Italy Q4-2022 🚗")

data_load_state = st.text("Loading data...")
data = load_data(1000)
data_load_state.text("Done! (using st.cache_data)")

if st.checkbox("Show raw data"):
    st.subheader("Raw data")
    st.write(data)

st.subheader("Number of cars by year")
# hist_values = np.histogram(data['anno'].dt.year, bins=10, range=(1980,2023))[0]
# st.bar_chart(hist_values)
fig, ax = plt.subplots()
sns.histplot(data=data["anno"].dt.year, bins=33, binrange=(1990, 2023), ax=ax)
st.pyplot(fig)
