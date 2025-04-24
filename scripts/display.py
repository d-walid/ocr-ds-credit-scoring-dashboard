import streamlit as st
import pandas as pd

from charts import local_features_graph, comparaison_between_clients_graph


def display_prediction_summary(prediction_result):
    st.header("Client Analysis - Results")
    prediction = prediction_result["prediction"][0]
    proba = prediction_result["proba_classe_1"]
                
    if prediction == 0:
        st.success(f"Credit granted (probability of payment default :  {proba:.2%})")
    else:
        st.error(f"Credit refused (probability of payment default : {proba:.2%})")
    return prediction


def display_client_analysis(prediction_result):
    top_features_df = pd.DataFrame(prediction_result["top_10_local_importance"])
    client_data = prediction_result["client_info"]
    global_data = pd.DataFrame(prediction_result["global_info"])
    selected_features = prediction_result["selected_features"]
    
    # Line 1 : Results of the analysis
    display_prediction_summary(prediction_result)
    st.markdown("---")
    
    # Line 2 : Graphs
    st.subheader("Key features for this client")
    local_features_graph(top_features_df)
    display_explanation_text()
        
    st.markdown("---")
    st.subheader("Comparaison between this client and the rest")
    col1, col2, col3 = st.columns(3)
    cols = [col1, col2, col3]
    
    for i, feature in enumerate(selected_features):
        with cols[i]:    
            comparaison_between_clients_graph(feature, client_data, global_data)
            
    
    
def display_explanation_text():
    st.markdown(
        "🔍 The bars above show the **main features** that influenced the model's decision.  \n"
        "➡️ A **positive** value (to the right) indicates the feature **pushed toward credit refusal**.  \n"
        "⬅️ A **negative** value (to the left) indicates it **pushed toward credit approval**.  \n"
        "ℹ️ Hover over each bar to see the **client’s value** and the **feature’s description**."
    )

