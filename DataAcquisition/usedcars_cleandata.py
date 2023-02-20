from datetime import datetime
import argparse
import regex as re
import os
import json
import pandas as pd
import numpy as np

main_columns = sorted(['Acconto', 'Anno', 'Carburante', 'Carrozzeria', 'Chilometraggio', 'Cilindrata_cm3', 'Cilindri',
                       'Colore', 'Comfort', 'Consumo_comb_L100km', 'Consumo_extraurb_L100km', 'Consumo_urb_L100km',
                       'Emissioni_CO2_gKm', 'Extra', 'Intrattenimento__Media', 'Marce', 'Peso_a_vuoto_kg',
                       'Porte', 'Posti', 'Prezzo_auto', 'Sicurezza', 'Tagliandi_certificati', 'Tipo_di_cambio',
                       'Tipo_di_veicolo', 'Trazione', 'city', 'country', 'countryCode', 'date', 'garanzia_mesi',
                       'makeId', 'maker', 'model', 'modelOrModelLineId', 'modelVersionInput', 'potenza_cv',
                       'potenza_kw', 'price', 'street', 'unico_proprietario', 'zip'
                       ]
                      )

path_to_added_batches = os.path.join("..", "data", "added_batches.json")
path_to_full_dataset = os.path.join("..", "data", "usedcars_dataset.csv")


def initWSCleaner():
    if not os.path.isdir(os.path.join("..", "data")):
        os.mkdir(os.path.join("..", "data"))

    if not os.path.isfile(path_to_added_batches):
        with open(path_to_added_batches, "w") as file:
            json.dump([], file)

    if not os.path.isfile(path_to_full_dataset):
        df = pd.DataFrame(columns=main_columns)
        df.to_csv(path_to_full_dataset, sep=";", index_label="url")


def getTargets(target, added_batches):

    if target:
        file_path = os.path.join("..", "data", target)
        # Filepath must be a .csv file, different from main dataset
        if os.path.isfile(file_path) and file_path.endswith(".csv") and file_path != path_to_full_dataset:
            target_list = [target]
        else:
            print("Target not found or inconsistent!")
            target_list = []
    else:
        # Target all csv in data folder
        target_list = [file for file in sorted(os.listdir(os.path.join("..", "data")))
                       if file.endswith(".csv") and file != "usedcars_dataset.csv"]

    target_list = [tar for tar in target_list if tar not in added_batches]

    return target_list


def edit_index_columns(df):
    "Sets index from URL and rename columns"
    df.index = df.index.str.strip('/annunci/')
    df.columns = df.columns.str.replace('\n', ' ', regex=False)
    df.columns = df.columns.str.replace(' ', '_', regex=False)
    for char in [';', '.', ',', ':', '/', '*']:
        df.columns = df.columns.str.replace(char, '', regex=False)

    col_rename_dict = {
        'Cilindrata': 'Cilindrata_cm3',
        'Consumo_di_carburante': 'Consumo_di_carburante_L100km',
        'Emissioni_CO₂': 'Emissioni_CO2_gKm',
        'Peso_a_vuoto': 'Peso_a_vuoto_kg',
        'Usato_garantito': 'garanzia_mesi',
        'Proprietari': 'unico_proprietario'
    }

    df = df.rename(columns=col_rename_dict)
    return df


def drop_columns(df):
    "Retains only columns from main_columns"
    col_to_remove = [col for col in df.columns if col not in main_columns]
    df = df.drop(columns=col_to_remove)
    return df

def add_missing_columns(df):
    "Add columns in main_columns not found in processed DataFrame, filled with None"
    col_to_add = [col for col in main_columns if col not in df.columns]
    for col in col_to_add:
        df[col] = None
    return df

def extract_text_data(df):
    "Applies regex to extract data from descriptions"

    price_pat = r'\€\s*(\d*),*'
    km_pat = r'(\d*)\s*km'
    pot_kw_pat = r'(\d*)\s*kW'
    pot_cv_pat = r'\((\d*)\s*CV\)'
    cil_cm3_pat = r'(\d*)\s*cm'
    weight_kg_pat = r'(\d*)\s*kg'
    emis_gkm_comb_pat = r'(\d*)\s*g/km\s*\(comb'
    garanzia_mesi_pat = r'(\d*)\s*mesi'
    consumo_comb_L100km_pat = r'(\d+\.?\d*)\sl/100\skm\s\(comb'
    consumo_urb_L100km_pat = r'(\d+\.?\d*)\sl/100\skm\s\(urb'
    consumo_extraurb_L100km_pat = r'(\d+\.?\d*)\sl/100\skm\s\(extraurb'

    df['Anno'] = pd.to_datetime(df['Anno'], format="%m/%Y")

    km_columns = ['Chilometraggio']
    price_columns = ['Prezzo_auto', 'price', 'Acconto']

    for col in km_columns:
        df[col] = df[col].str.replace('.', '', regex=False).str.extract(
            pat=km_pat).astype(np.float64)

    for col in price_columns:
        df[col] = df[col].str.replace('.', '', regex=False).str.extract(
            pat=price_pat).astype(np.float64)

    df['Cilindrata_cm3'] = df['Cilindrata_cm3'].str.replace(
        '.', '', regex=False).str.extract(pat=cil_cm3_pat).astype(np.float64)
    df['potenza_kw'] = df['Potenza'].str.replace(
        '.', '', regex=False).str.extract(pat=pot_kw_pat).astype(np.float64)
    df['potenza_cv'] = df['Potenza'].str.replace(
        '.', '', regex=False).str.extract(pat=pot_cv_pat).astype(np.float64)

    df['Peso_a_vuoto_kg'] = df['Peso_a_vuoto_kg'].str.replace(
        '.', '', regex=False).str.extract(pat=weight_kg_pat).astype(np.float64)
    df['Emissioni_CO2_gKm'] = df['Emissioni_CO2_gKm'].str.replace(
        '.', '', regex=False).str.extract(pat=emis_gkm_comb_pat).astype(np.float64)
    df['garanzia_mesi'] = df['garanzia_mesi'].str.extract(
        pat=garanzia_mesi_pat).astype(np.float64)

    df['Consumo_comb_L100km'] = df['Consumo_di_carburante_L100km'].str.replace(
        ',', '.', regex=False).str.extract(pat=consumo_comb_L100km_pat, expand=False).astype(np.float64)
    df['Consumo_urb_L100km'] = df['Consumo_di_carburante_L100km'].str.replace(
        ',', '.', regex=False).str.extract(pat=consumo_urb_L100km_pat, expand=False).astype(np.float64)
    df['Consumo_extraurb_L100km'] = df['Consumo_di_carburante_L100km'].str.replace(
        ',', '.', regex=False).str.extract(pat=consumo_extraurb_L100km_pat, expand=False).astype(np.float64)

    return df


def replace_values(df):
    "Edits categorical and boolean columns"

    # replace 0 with nan in fuel consumption
    df['Consumo_comb_L100km'] = np.where(df['Consumo_comb_L100km']<0.1, np.nan, df['Consumo_comb_L100km'])
    df['Consumo_urb_L100km'] = np.where(df['Consumo_urb_L100km']<0.1, np.nan, df['Consumo_urb_L100km'])
    df['Consumo_extraurb_L100km'] = np.where(df['Consumo_extraurb_L100km']<0.1, np.nan, df['Consumo_extraurb_L100km'])

    # Extract fuel category: Benzina, Diesel, Ibrida, Elettrica, GPL, Metano, Altro
    df['Carburante'] = df['Carburante'].map(getFuel)
    df['Carburante'] = np.where(df['Altre_fonti_energetiche'].str.contains('elettr').notnull(), 'Ibrida', df['Carburante'])

    # Extract car body category: Suv/Fuoristrada, Berlina, Station Wagon, City Car, Furgone, Coupe, Cabrio, Altro
    df['Carrozzeria'] = df['Carrozzeria'].map(getCarBody)

    # Boolean columns: Only Owner, Certified Checks
    df['Tagliandi_certificati'] = np.where(df['Tagliandi_certificati']=='Sì', True, False)
    df['unico_proprietario'] = np.where(df['unico_proprietario']<1.1, True, False)

    #Replace 4x4 with Integrale (wheel driven)
    df['Trazione'] = df['Trazione'].replace(regex='4x4', value='Integrale')

    return df


def clean_data(df):
    df = edit_index_columns(df)
    df = add_missing_columns(df)
    df = extract_text_data(df)
    df = replace_values(df)
    df = drop_columns(df)
    return df

def getFuel(fuelString):

    if not isinstance(fuelString, str):
        return 'Altro'

    fuelString = fuelString.lower()
    if 'benz' in fuelString:
        fuelType = 'Benzina'
    elif 'super' in fuelString:
        fuelType = 'Benzina'
    elif 'diesel' in fuelString:
        fuelType = 'Diesel'
    elif 'gpl' in fuelString:
        fuelType = 'GPL'
    elif 'liqu' in fuelString:  # gas di petrolio liquefatto
        fuelType = 'GPL'
    elif 'metano' in fuelString:
        fuelType = 'Metano'
    elif 'naturale' in fuelString:
        fuelType = 'Metano'
    elif 'elettr' in fuelString:
        fuelType = 'Elettrica'
    else:
        fuelType = 'Altro'

    return fuelType


def getCarBody(carBodyString):

    if not isinstance(carBodyString, str):
        return 'Altro'

    carBodyString = carBodyString.lower()
    if 'suv' in carBodyString:
        carBodyType = 'SUV/Fuoristrada'
    elif 'fuoristrada' in carBodyString:
        carBodyType = 'SUV/Fuoristrada'
    elif 'wagon' in carBodyString:
        carBodyType = 'Station Wagon'
    elif 'city' in carBodyString:
        carBodyType = 'City Car'
    elif 'berl' in carBodyString:
        carBodyType = 'Berlina'
    elif 'cabrio' in carBodyString:
        carBodyType = 'Cabrio'
    elif 'coup' in carBodyString:
        carBodyType = 'Coupe'
    elif 'mono' in carBodyString:
        carBodyType = 'Monovolume'
    elif 'furg' in carBodyString:
        carBodyType = 'Furgone'
    else:
        carBodyType = 'Altro'

    return carBodyType


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--target', '-t', dest='target',
                        help='Append only a specific target file from data folder')
    parser.add_argument('--refresh', '-r', dest='refresh',
                        help='Refresh the full dataset', action='store_true')
    parser.add_argument('--debug', '-d', dest='debug',
                        help='Enable debug mode', action='store_true')

    args = parser.parse_args()
    target = args.target
    refresh = args.refresh
    db = args.debug

    # Check/Create folders for results
    initWSCleaner()
    if refresh:
        added_batches = []
        df_main = pd.DataFrame(columns=main_columns)
    else:
        with open(path_to_added_batches) as file:
            added_batches = json.load(file)
        df_main = pd.read_csv(path_to_full_dataset, sep=";", index_col='url')

    # Getting target list
    targets = getTargets(target, added_batches)
    if not targets:
        print("No targets!")
        exit()
    print(f"Target batches: {targets}")

    # Processing target datasets
    for ii, tar in enumerate(targets):
        df = pd.read_csv(os.path.join("..", "data", tar), sep=";", index_col='url')
        print(f"Processing dataset {tar} ({ii+1}/{len(targets)})", end="\r")
        try:
            df = clean_data(df)
            added_batches.append(tar)
        except Exception as e:
            print(f"Error in dataset {tar}: {e}")
            continue
        df_main = pd.concat([df_main, df])

    #Dropping duplicates
    df_main = df_main[~df_main.index.duplicated(keep='first')]

    print("\nAll targets processed")
    print(f"Main dataset now contains {len(df_main)} records")
    # Saving results
    if len(targets) > 0:
        df_main.to_csv(path_to_full_dataset, sep=";",index_label="url")
        with open(path_to_added_batches, "w") as file:
            json.dump(added_batches, file)
