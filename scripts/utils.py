import os
import requests
import numbers
import streamlit as st
import pandas as pd


def load_feature_description():
    """
    Load the feature descriptions from a CSV file and return them as a dictionary.
    """
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DEF_FEATURES_PATH = os.path.join(BASE_DIR, "..", "data", "dashboard", "definition_features.csv")
    df_def_features = pd.read_csv(DEF_FEATURES_PATH, sep=";")
    return dict(zip(df_def_features["row"], df_def_features["description"]))

feature_descriptions = load_feature_description()


def get_feature_description(feature_name):
    return feature_descriptions.get(feature_name, "Description not available.")


def setup_page():
    ## Set the page configuration for the Streamlit app
    st.set_page_config(
        page_title="Credit Scoring Dashboard",
        layout="wide"
    )

    # Set the title and description of the app
    st.title("Credit Scoring Dashboard")
    st.markdown(
        "This tool estimates the probability of a client defaulting on their credit. "
        "To get started, enter a client ID in the input field on the left."    
    )
    

def get_prediction(client_id):
    """
    Send a request to the API to get the prediction for the given client ID.
    The API is expected to return a JSON response with the prediction result.
    """

    api_url = "http://127.0.0.1:5000/predict"
    response = requests.post(api_url, json={"SK_ID_CURR": client_id})

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        st.error(f"Erreur : {response.status_code} - {response.text}")
        return None
    
    
def format_value(val):
    """
    Format the value for display in the Streamlit app.
    """

    if pd.isnull(val):
        return ""
    elif isinstance(val, numbers.Number) and float(val).is_integer():
        return f"{int(val)}"
    elif isinstance(val, numbers.Number):
        return f"{val:.2f}"
    else:
        return str(val)