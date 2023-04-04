import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import serving_helpers
import altair as alt

st.title("Used Cars in Italy Q4-2022 🚗")

data_load_state = st.text("Loading data...")
data = serving_helpers.load_data(20000)
data_load_state.text("Done! (using st.cache_data)")

# Gauges section
num_offers, median_price, median_age = serving_helpers.get_gauges()

col1, col2, col3 = st.columns(3)
col1.metric("Number of Offers Tracked", num_offers)
col2.metric("Median Price", median_price)
col3.metric("Median Age", median_age)

# Top 10 Charts Section
top_selling = serving_helpers.get_top_selling_models(10)
top_value = serving_helpers.get_top_value_makers(10)

col1, col2 = st.columns(2)
with col1:
    st.subheader("Top 10 selling cars")
    top_selling = top_selling.style.format(precision=0, thousands=" ")
    st.write(top_selling)

with col2:
    st.subheader("Top 10 most valuable makers")
    top_value = top_value.style.format(
        precision=0, thousands=" ", formatter={"Sum of Prices (Million €)": "{:.0f}"}
    )
    st.write(top_value)

# Offers by year section
st.subheader("Number of cars by year")
cars_by_year_df = serving_helpers.get_car_counts_by_year_and_bodytype(30)
cars_by_year_chart = (
    alt.Chart(cars_by_year_df)
    .mark_bar()
    .encode(
        x=alt.X("Year:N", title="Year"),
        y=alt.Y("sum(Counts)", title="Counts"),
        color="Body Type",
    )
)
st.altair_chart(cars_by_year_chart, theme="streamlit")

# Price by year section
st.subheader("Price distribution by year")
st.caption(r"Median, $25^{\text{th}}$ and $75^{\text{th}}$ percentiles")
price_by_year_df = serving_helpers.get_car_prices_by_year(30)
price_by_year_area = (
    alt.Chart(price_by_year_df)
    .mark_area(opacity=0.3)
    .encode(
        x=alt.X("anno:N", title="Year"), y="q_min", y2="q_max"
    )
)
price_by_year_line = alt.Chart(price_by_year_df).mark_line().encode(
    x="anno:N",
    y=alt.Y("median", title="Price (€)")
)

price_by_year_chart = price_by_year_area + price_by_year_line
st.altair_chart(price_by_year_chart, theme="streamlit")

# Raw data section
if st.checkbox("Show raw data"):
    st.subheader("Raw data")
    st.write(data)
