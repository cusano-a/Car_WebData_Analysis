import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import serving_helpers

st.title("Used Cars in Italy Q4-2022 🚗")

data_load_state = st.text("Loading data...")
data = serving_helpers.load_data(20000)
data_load_state.text("Done! (using st.cache_data)")

top_selling = serving_helpers.get_top_selling_models(10)
top_value = serving_helpers.get_top_value_makers(10)

col1, col2 = st.columns(2)
with col1:
    st.write(top_selling)

with col2:
    st.write(top_value)

st.subheader("Number of cars by year")
# hist_values = np.histogram(data['anno'].dt.year, bins=10, range=(1980,2023))[0]
# st.bar_chart(hist_values)
fig, ax = plt.subplots()
sns.histplot(data=data["anno"].dt.year, bins=33, binrange=(1990, 2023), ax=ax)
st.pyplot(fig)


if st.checkbox("Show raw data"):
    st.subheader("Raw data")
    st.write(data)
