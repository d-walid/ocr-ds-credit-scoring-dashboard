# 🧠 Credit Scoring Dashboard

Ce projet a pour objectif de proposer une **application web de scoring crédit** à destination d’un public **non technique**. Elle permet d’estimer le risque de défaut d’un client et de visualiser ses caractéristiques comparées à celles d'autres clients.  

## 🔍 Fonctionnalités

- Estimation de la probabilité de défaut d’un client à partir de son identifiant
- Affichage de la décision (accepté/refusé)
- Comparaison visuelle du client avec les clients acceptés et refusés
- Explication du score via des graphiques
- Description des variables utilisées

## 🧱 Architecture

- **Backend** : une API Flask déployée sur Render
- **Frontend** : une interface Streamlit déployée sur Streamlit Cloud
- **Modèle** : LightGBM, intégré dans une pipeline scikit-learn

## 🖥️ Lancement local

### Prérequis

- Python 3.11
- pip, virtualenv (ou autre gestionnaire d’environnement)

### Installation

```python
git clone https://github.com/d-walid/ocr-ds-credit-scoring-dashboard.git
cd ocr-ds-credit-scoring-dashboard

# Création de l’environnement
python -m venv venv
source venv/bin/activate
.\venv\Scripts\activate # Windows

# Installation des dépendances
pip install -r requirements.txt
```

### Lancement
```python
# API Flask
python scripts/app.py

# Application Streamlit
streamlit run scripts/streamlit_app.py
```