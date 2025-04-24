import pandas as pd
import plotly.express as px
import streamlit as st
from utils import format_value, get_feature_description


def local_features_graph(top_features_df: pd.DataFrame):
    top_features_df["description"] = top_features_df["feature"].apply(get_feature_description)
    
    fig = px.bar(
        top_features_df,
        x="shap_value",
        y="feature",
        orientation="h",
    )
    
    fig.update_traces(
        text=top_features_df["value"].apply(format_value),
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Value : %{text}<br>Description : %{customdata}<extra></extra>",
        customdata=top_features_df["description"]
    )
                   
    fig.update_layout(
        title="Top features influencing the decision",
        xaxis_title="Value",
        yaxis_title="Feature",
        xaxis=dict(showticklabels=False, title=None),
        yaxis=dict(autorange="reversed")
    )  
    
    st.plotly_chart(fig)
    return fig
    

def comparaison_between_clients_graph(feature_name, client_data, global_data):
    fig = px.histogram(
        global_data,
        x=feature_name,
        nbins=30,
        title=f"Distribution : {feature_name}",
        labels={feature_name : feature_name}
    )
    
    fig.add_vline(
        x=client_data[feature_name],
        line_dash="dash",
        line_color="red",
        annotation_text="Client",
        annotation_position="top right",
        annotation_y=1.05
    )
    
    fig.update_layout(
    )
    
    st.plotly_chart(fig)
    return fig