import os
import requests
import streamlit as st
import pandas as pd


def load_feature_description():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DEF_FEATURES_PATH = os.path.join(BASE_DIR, "..", "data", "dashboard", "definition_features_fr.csv")
    df_def_features = pd.read_csv(DEF_FEATURES_PATH, sep=";")
    return dict(zip(df_def_features["row"], df_def_features["description_fr"]))

feature_descriptions = load_feature_description()

def get_feature_description(feature_name):
    return feature_descriptions.get(feature_name, "Description non disponible.")


def setup_page():
    ## Config page
    st.set_page_config(
        page_title="Modèle de scoring de crédit",
        layout="wide"
    )

    st.title("Tableau de bord de scoring de crédit")
    st.markdown("Cet outil permet d'évaluer la probabilité de défaut de paiement d'un client.")
    

def get_prediction(client_id):
    api_url = "http://127.0.0.1:5000/predict"
    response = requests.post(api_url, json={"SK_ID_CURR": client_id})
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        st.error(f"Erreur : {response.status_code} - {response.text}")
        return None
    
    
def format_value(val):
    if pd.isnull(val):
        return ""
    elif isinstance(val, float) and val.is_integer():
        return f"{int(val)}"
    elif isinstance(val, (int, float)):
        return f"{val:.2f}"
    else:
        return str(val)
