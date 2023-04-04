import streamlit as st

st.set_page_config(
    page_title="Home",
    page_icon="🏠",
)

st.write("# Welcome! 👋")

st.markdown(
    """
    This is a personal project about the used cars market in Italy. It currently includes:
    - Dashboard
    - Car Evaluator

    **👈 Select a page from the sidebar**

    ### Dashboard
    A simple Dashboard describing the data collected for this project.
    The data were collected from December 2022 to April 2023 from a large European online car market.
    However only offers from Italy were collected.

    ### Car Evaluator
    The data collected were used to generate a Machine Learning model to predict the expected car price given the most important car features.
    The model is an Extreme Gradient Boosting Trees model. The features needed include the car model, age and power.
    \n
    You can insert the features of your car to obtain a real time estimate of its value.


"""
)
