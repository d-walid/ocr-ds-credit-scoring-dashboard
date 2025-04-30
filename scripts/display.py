import streamlit as st
import pandas as pd
from charts import local_features_graph, comparison_between_clients_graph


def display_prediction_summary(prediction_result):
    """
    Display the prediction summary based on the prediction result.
    If the prediction is 0, it indicates credit granted; otherwise, credit refused.
    The probability of payment default is also displayed.
    """

    st.header("Client Analysis - Results")
    prediction = prediction_result["prediction"][0]
    proba = prediction_result["proba_classe_1"]

    if prediction == 0:
        st.success(f"Credit granted (probability of payment default :  {proba:.2%})")
    else:
        st.error(f"Credit refused (probability of payment default : {proba:.2%})")
    return prediction


def show_comparison(title, features, client_data, global_data):
    """
    Show the comparison between the client data and the global data for the selected features.
    The comparison is displayed in three columns.
    Each column contains a histogram for the feature distribution in the global data.
    """

    st.markdown(f"#### {title}")
    col1, col2, col3 = st.columns(3)
    cols = [col1, col2, col3]

    for i, feature in enumerate(features):
        with cols[i]:
            comparison_between_clients_graph(feature, client_data, global_data)


def display_client_analysis(prediction_result):
    """
    Display the analysis of the client based on the prediction result.
    The analysis includes the top 10 features influencing the decision, the client's data, and the comparison 
    with accepted and refused clients.
    """

    top_features_df = pd.DataFrame(prediction_result["top_10_local_importance"])
    client_data = prediction_result["client_info"]
    global_data = pd.DataFrame(prediction_result["global_info"])
    global_data_accepted = global_data[global_data["TARGET"] == 0]
    global_data_refused = global_data[global_data["TARGET"] == 1]
    selected_features = prediction_result["selected_features"]
    
    # Display the client's summary data 
    display_prediction_summary(prediction_result)
    st.markdown("---")
    st.subheader("Key features for this client")

    # Display the top features influencing the decision if the client is accepted or refused
    local_features_graph(top_features_df)
    display_explanation_text()

    # Display the comparison between the client data and the global data for the top 3 selected features
    st.markdown("---")
    prediction = prediction_result["prediction"][0]
    if prediction == 1:
        show_comparison("Compared to refused clients", selected_features, client_data, global_data_refused)
        show_comparison("Compared to accepted clients", selected_features, client_data, global_data_accepted)
    else:
        show_comparison("Compared to accepted clients", selected_features, client_data, global_data_accepted)

    # Display a text summary of the client's profile compared to others
    st.subheader("Summary of the client's profile compared to others")
    summaries = generate_comparison_summary(selected_features, client_data, global_data_accepted, global_data_refused, prediction)
    for summary in summaries:
        st.markdown(f"- {summary}")
    st.markdown("---")
            

def display_explanation_text():
    st.markdown(
        "🔍 The bars above show the **main features** that influenced the model's decision.  \n"
        "➡️ A **positive** value (to the right) indicates the feature **pushed toward credit refusal**.  \n"
        "⬅️ A **negative** value (to the left) indicates it **pushed toward credit approval**.  \n"
        "ℹ️ Hover each bar to see the **client’s value** and the **feature’s description**."
    )


def generate_comparison_summary(selected_features, 
                                client_data, 
                                global_data_accpeted, 
                                global_data_refused, 
                                prediction):
    """
    Generate a summary of the client's profile compared to accepted and refused clients.
    The summary includes some texts who llustrate the client's position relative to the average of accepted and refused clients.
    The summary is based on the selected features and the prediction result.
    """

    summaries = []
    for feature in selected_features:
        client_value = client_data[feature]
        accepted_mean = global_data_accpeted[feature].mean()
        refused_mean = global_data_refused[feature].mean()

        if prediction == 0:
            comparison = "above" if client_value > accepted_mean else "below"
            summaries.append(f"For **{feature}**, the client is **{comparison}** the average of accepted clients.")
        else:
            comparison_refused = "above" if client_value > refused_mean else "below"
            comparison_accepted = "above" if client_value > accepted_mean else "below"
            summaries.append(
                f"For **{feature}**, the client is **{comparison_refused}** the average of refused clients "
                f"and **{comparison_accepted}** the average of accepted clients."
            )

    return summaries
