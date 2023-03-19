import pandas as pd
import numpy as np
import os
import streamlit as st
import joblib


@st.cache_data
def load_data(nrows: int):
    columns = [
        "maker",
        "model",
        "Anno",
        "Chilometraggio",
        "potenza_cv",
        "Carburante",
        "price",
    ]
    data = pd.read_csv(
        os.path.join("..", "data", "usedcars_dataset.csv"),
        nrows=nrows,
        sep=";",
        usecols=columns,
    )
    data = data.dropna()
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    data["anno"] = pd.to_datetime(data["anno"])
    return data


@st.cache_resource
def load_model():
    model_path = os.path.join("..", "Modeling", "models", "XGB_final.joblib")
    with open(model_path, "rb") as model_file:
        model = joblib.load(model_file)
    return model


model = load_model()


@st.cache_data
def make_prediction(inputs: dict):
    prediction = model.predict(pd.DataFrame.from_dict(inputs))[0]
    return prediction


@st.cache_data
def pack_inputs(**inputs_unpacked):
    inputs_packed = {key: [value] for key, value in inputs_unpacked.items()}
    return inputs_packed

@st.cache_data
def get_makers(num_makers=40):
    data = load_data(None)
    makers = data.value_counts(['maker']).sort_values(ascending=False)
    num_makers= min(len(makers), num_makers)
    makers = makers.reset_index().loc[:num_makers, 'maker'].to_numpy()
    return np.sort(makers)

@st.cache_data
def get_models(maker, num_models=30):
    data = load_data(None).query("maker==@maker")
    models = data.value_counts(['model']).sort_values(ascending=False)
    num_models = min(len(models), num_models)
    models = models.reset_index().loc[:num_models, 'model'].to_numpy()
    return np.sort(models)
