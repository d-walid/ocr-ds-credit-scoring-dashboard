# 🧠 Credit Scoring Dashboard

This project aims to provide a **web-based credit scoring application** designed for a non-technical audience. It estimates a client's default risk and visualizes their profile compared to other clients.

## 🔍 Features

- Estimate the probability of default based on multiples informations
- Display the credit decision (approved/rejected)
- Visual comparison between the client and approved/rejected clients
- Score explanation through visualizations
- Description of the variables used to help the non-technical audience

## 🧱 Architecture

- **Backend** : Flask API deployed on Render
- **Frontend** : Streamlit interface deployed on Streamlit Cloud
- **Model** : LightGBM, integrated into a scikit-learn pipeline

## 🖥️ Run Locally

### Prerequisites

- Python 3.11
- pip, virtualenv (or another environment manager)

### Installation

```
git clone https://github.com/d-walid/ocr-ds-credit-scoring-dashboard.git
cd ocr-ds-credit-scoring-dashboard

# Create virtual environment
python -m venv venv
source venv/bin/activate
.\venv\Scripts\activate # Windows

# Install dependencies
pip install -r requirements.txt
```

### Run the app
```
# Flask API
python scripts/app.py

# Streamlit application
streamlit run scripts/streamlit_app.py
```
