import pandas as pd
import numpy as np
import os
import streamlit as st
import joblib
from datetime import datetime


@st.cache_data
def filter_usedcars_data(
    df, max_price=1e6, min_price=100, max_cv=1000, max_km=1e6, max_engsize=1e4
):
    df = df.query(
        "~((potenza_cv > @max_cv or potenza_cv < 0) \
                                or (Chilometraggio>@max_km or Chilometraggio < 0) \
                                or (price > @max_price or price < @min_price ) \
                                or (Cilindrata_cm3 > @max_engsize or Cilindrata_cm3 < 0 ) \
                    )"
    )
    return df


@st.cache_data
def load_data(nrows: int):
    columns = [
        "date",
        "maker",
        "model",
        "Anno",
        "Chilometraggio",
        "potenza_cv",
        "Carburante",
        "Carrozzeria",
        "Cilindrata_cm3",
        "Tipo_di_cambio",
        "Trazione",
        "price",
    ]
    data = pd.read_csv(
        os.path.join("..", "data", "usedcars_dataset.csv"),
        nrows=nrows,
        sep=";",
        usecols=columns,
    )
    data = data.dropna()
    data = filter_usedcars_data(data)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    data["anno"] = pd.to_datetime(data["anno"])
    data["date"] = pd.to_datetime(data["date"])
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
    makers = data.value_counts(["maker"]).sort_values(ascending=False)
    num_makers = min(len(makers), num_makers)
    makers = makers.reset_index().loc[:num_makers, "maker"].to_numpy()
    return np.sort(makers)


@st.cache_data
def get_models(maker, num_models=30):
    data = load_data(None).query("maker==@maker")
    models = data.value_counts(["model"]).sort_values(ascending=False)
    num_models = min(len(models), num_models)
    models = models.reset_index().loc[:num_models, "model"].to_numpy()
    return np.sort(models)


@st.cache_data
def get_aggregates_by_model():
    data = load_data(None)
    aggregated_data = (
        data.groupby(["maker", "model"])
        .agg(
            model_count=pd.NamedAgg(column="model", aggfunc="count"),
            price_sum=pd.NamedAgg(column="price", aggfunc="sum"),
        )
        .reset_index()
    )
    return aggregated_data


@st.cache_data
def get_top_selling_models(num_models=10):
    df = get_aggregates_by_model()
    df = df.sort_values(by="model_count", ascending=False)
    df = df.head(num_models)
    df["maker_model"] = df["maker"] + " " + df["model"]
    df = df[["maker_model", "model_count"]]
    df = df.rename(columns={"maker_model": "Model", "model_count": "Number of Offers"})
    df.index = np.arange(1, len(df) + 1)
    return df


@st.cache_data
def get_top_value_makers(num_makers=10):
    df = get_aggregates_by_model()
    df = df.groupby(by="maker").agg({"price_sum": "sum"})
    df = df.sort_values(by="price_sum", ascending=False).reset_index().head(num_makers)
    df["price_sum"] = df["price_sum"] * 1e-6
    df = df.rename(columns={"maker": "Maker", "price_sum": "Sum of Prices (Million €)"})
    df.index = np.arange(1, len(df) + 1)
    return df


@st.cache_data
def get_car_counts_by_year(num_years=30):
    data = load_data(None)
    df = data["anno"].dt.year.value_counts()
    df = df.rename_axis("Year").reset_index(name="Counts")
    if num_years:
        df = df.head(num_years)
    return df


@st.cache_data
def get_car_counts_by_year_and_bodytype(num_years=30):
    data = load_data(None)
    df = (
        data.groupby([data["anno"].dt.year, "carrozzeria"])
        .count()
        .rename(columns={"anno": "Counts"})["Counts"]
        .reset_index()
    )
    df = df.rename(columns={"anno": "Year", "carrozzeria": "Body Type"})
    if num_years:
        year_limit = datetime.now().year - num_years
        df = df.query("Year>@year_limit")
    return df


@st.cache_data
def get_car_prices_by_year(num_years=30):
    data = load_data(None)
    df = (
        data.groupby(data["anno"].dt.year)
        .agg(
            q_min=pd.NamedAgg(column="price", aggfunc=lambda x: x.quantile(0.25)),
            q_max=pd.NamedAgg(column="price", aggfunc=lambda x: x.quantile(0.75)),
            median=pd.NamedAgg(column="price", aggfunc="median"),
        )
        .reset_index()
    )
    df["anno"] = df["anno"].astype("int64")
    if num_years:
        df = df.tail(num_years)
    print(df.dtypes)
    return df

@st.cache_data
def get_gauges():
    data = load_data(None)
    num_offers = f"{len(data):d}"
    median_price = f"{data['price'].median():.0f} €"
    median_age = ((data['date']-data['anno']).median())/ np.timedelta64(1, 'Y')
    median_age = f"{median_age:.1f} Y"
    return num_offers, median_price, str(median_age)
