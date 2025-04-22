import streamlit as st
import pandas as pd
import plotly.express as px 
from utils import setup_page, get_prediction, format_value, get_feature_description


## 440159
## 376404
## 195580
## 182619
## 242729
## 221248
## 384066
setup_page()


def display_client_analysis(prediction_result):
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("Résultat de l'analyse du client")
        prediction = prediction_result["prediction"][0]
        proba = prediction_result["proba_classe_1"]
                    
        if prediction == 0:
            st.success(f"Crédit accordé (probabilité de défaut de paiement : {proba:.2%})")
        else:
            st.error(f"Crédit refusé (probabilité de défaut de paiement : {proba:.2%})")
            
        
    display_explanation_text()
    st.markdown("---")
    st.subheader("Caractéristiques importantes pour ce client")
    top_features_df = pd.DataFrame(prediction_result["top_10_local_importance"])
    top_features_df["description_fr"] = top_features_df["feature"].apply(get_feature_description)
                
    fig = px.bar(
        top_features_df,
        x="shap_value",
        y="feature",
        orientation="h",
    )
    
    fig.update_traces(
        text=top_features_df["value"].apply(format_value),
        textposition="outside",
        hovertemplate="Description : %{customdata}",
        customdata=top_features_df["description_fr"]
    )
                   
    fig.update_layout(
        title="Variables ayant influé sur la décision",
        xaxis_title="Valeur",
        yaxis_title="Variable",
        xaxis=dict(showticklabels=False, title=None),
        yaxis=dict(autorange="reversed")
    )  
    st.plotly_chart(fig)
    
    
    
def handle_client_selection():
    st.sidebar.header("Sélectionner un client")
    client_id = st.sidebar.text_input(
        "Entrez l'identifiant d'un client :"
    )

    if st.sidebar.button("Analyser ce client"):
        try:
            client_id = int(client_id)
            with st.spinner("Analyse en cours..."):
                prediction_result = get_prediction(client_id)
                
                if prediction_result:
                    display_client_analysis(prediction_result)
                    
        except ValueError:
            st.error("Veuillez entrer un identifiant valide.")
            

def display_explanation_text():
    st.markdown(
        "🔍 Les barres ci-dessous représentent les **principales variables** ayant influencé la décision.  \n"
        "🧭 Certaines ont pu pousser vers l'acceptation, d'autres vers le refus.  \n"
        "ℹ️ Survolez une barre pour voir sa description et la valeur du client."
    )


handle_client_selection()