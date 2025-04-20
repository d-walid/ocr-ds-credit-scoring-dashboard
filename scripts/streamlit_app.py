import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px 
import plotly.graph_objects as go
import requests
import json

## Config page
st.set_page_config(
    page_title="Modèle de scoring de crédit",
    layout="wide"
)


## App's title
st.title("Tableau de bord de scoring de crédit")
st.markdown("Cet outil permet d'évaluer la probabilité de défaut de paiement d'un client")


def get_prediction(client_id):
    api_url = "https://ocr-model-scoring-d21bdbd88983.herokuapp.com/predict"
    response = requests.post(api_url, json={"SK_ID_CURR": client_id})
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        st.error(f"Erreur : {response.status_code} - {response.text}")
        return None
    

st.sidebar.header("Sélectionner un client")
client_id = st.sidebar.text_input(
    "Entrez l'ID du client :"
)

if st.sidebar.button("Analyser ce client"):
    try:
        client_id = int(client_id)
        with st.spinner("Analyse en cours..."):
            prediction_result = get_prediction(client_id)
            
            if prediction_result:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.header("Résultat de l'analyse du client")
                    prediction = prediction_result["prediction"][0]
                    proba = prediction_result["proba_classe_1"]
                    
                    if prediction == 0:
                        st.success(f"Crédit accordé (probabilité de défaut de paiement : {proba:.2%})")
                    else:
                        st.error(f"Crédit refusé (probabilité de défaut de paiement : {proba:.2%})")
                        
                st.header("Caractéristiques importantes pour ce client")
                top_features = prediction_result["top_10_local_importance"]
                
                fig = px.bar(
                    top_features,
                    x="shap_value",
                    y="feature",
                    orientation="h" 
                )
                fig.update_layout(coloraxis_showscale=False)
                fig.update_yaxes(categoryorder="total ascending")
                st.plotly_chart(fig)
                
    except ValueError:
        st.error("Veuillez entrer un ID client valide.")