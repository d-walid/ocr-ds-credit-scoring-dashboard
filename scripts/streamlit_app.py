import streamlit as st

from utils import setup_page, get_prediction
from display import display_client_analysis


## 440159
## 376404
## 195580
## 182619
## 242729
## 221248
## 384066
setup_page()


def handle_client_selection():
    st.sidebar.header("Select a client")
    client_id = st.sidebar.text_input(
        "Enter the client ID :"
    )

    if st.sidebar.button("Analyze this client"):
        try:
            client_id = int(client_id)
            with st.spinner("Analyzing..."):
                prediction_result = get_prediction(client_id)
                
                if prediction_result:
                    display_client_analysis(prediction_result)
                    
        except ValueError:
            st.error("Please enter a valid client ID.")


handle_client_selection()