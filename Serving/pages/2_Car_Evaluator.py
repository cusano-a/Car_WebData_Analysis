import streamlit as st
import datetime
import serving_helpers

makers_list = serving_helpers.get_makers()
body_types_list = ['Berlina','SUV/Fuoristrada','Station Wagon','City Car', 'Monovolume', 'Coupe', 'Furgone','Cabrio']
fuel_types_list = ["Benzina", "Diesel", "Metano", "GPL", "Ibrida", "Elettrica"]
gear_list = ["Manuale", "Automatico", "Semiautomatico"]
drive_wheel_list = ['Anteriore', 'Posteriore', 'Integrale']


def main():
    st.title("Used Cars Price Evaluator 💵")

    st.markdown(
        """
        Evaluate the market price of your car filling the form below 👇
        \n
        \n
    """
    )

    col1, col2 = st.columns(2)

    # Maker and model details
    maker = col1.selectbox(
        "Maker",
        options=makers_list,
    )

    if maker:
        models_list = serving_helpers.get_models(maker=maker)
        model = col2.selectbox(
            "Model",
            options=models_list,
        )

    # Age status of car details
    date_first_registration = col1.date_input(
        "Registration Date",
        min_value=datetime.date(1980, 1, 1),
        max_value=datetime.date.today(),
        help="The first date when the car was registerd",
    )
    age_years = (datetime.date.today() - date_first_registration).days / 365.0

    mileage = col2.number_input(
        "Mileage (Km)",
        value=40000,
        min_value=0,
        max_value=1000000,
        step=10000,
        format="%i",
    )

    # Engine Details
    power_cv = col1.number_input(
        "Power (CV)",
        value=100,
        min_value=0,
        max_value=2000,
        step=10,
        format="%i",
    )

    engine_size = col2.number_input(
        r"Engine size (cm$^3$)",
        value=1500,
        min_value=0,
        max_value=10000,
        step=100,
        format="%i",
    )

    fuel_type = col1.selectbox(
        "Fuel Type",
        options=fuel_types_list,
    )

    # Body details
    body_type = col2.selectbox(
        "Body Type",
        options=body_types_list,
    )

    gear_type = col1.selectbox(
        "Gear Type",
        options=gear_list,
    )

    drive_wheel = col2.selectbox(
        "Drive Wheel",
        options=drive_wheel_list,
    )

    inputs = serving_helpers.pack_inputs(
        Carburante=fuel_type,
        Carrozzeria=body_type,
        Chilometraggio=mileage,
        Cilindrata_cm3=engine_size,
        Cilindri=None,
        Consumo_comb_L100km=None,
        Marce=None,
        Peso_a_vuoto_kg=None,
        Porte=None,
        Posti=None,
        Tipo_di_cambio=gear_type,
        Tipo_di_veicolo="Usato",
        Trazione=drive_wheel,
        maker=maker,
        model=model,
        potenza_cv=power_cv,
        age_years=age_years,
    )

    if st.button("Submit"):
        price = round(serving_helpers.make_prediction(inputs))
        st.balloons()
        st.metric(label="Estimated value", value=str(price)+'€')



if __name__ == "__main__":
    main()
