from flask import request, jsonify
import joblib
import shap
import numpy as np 
import pandas as pd
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def load_model_and_data():
    # Paths to the model and data
    model_path = os.path.join(BASE_DIR, "..", "models", "LGBMClassifier_model.joblib")
    df_path = os.path.join(BASE_DIR, "..", "data", "dashboard", "df_sample.csv")

    # Load the model and data
    model = joblib.load(model_path)
    df = pd.read_csv(df_path, sep=";", encoding="utf-8")
    return model, df

model, df = load_model_and_data()


def prepare_explainer_and_features(model, df):
    # Prepare the explainer and features
    clf = model.named_steps["clf"]
    feature_names = df.drop(columns=["TARGET", "SK_ID_CURR"], errors="ignore").columns.tolist()
    explainer = shap.TreeExplainer(clf)
    return clf, feature_names, explainer

clf, feature_names, explainer = prepare_explainer_and_features(model, df)


## Routes
def register_routes(app):
    @app.route("/")
    def home():
        return "Bienvenue sur l'API."


    @app.route("/predict", methods=["POST"])
    def predict():
        # Get the data from the request
        data = request.get_json()
        sk_id = data["SK_ID_CURR"]

        # Drop the SK_ID_CURR and TARGET columns from the dataframe
        X = df[df["SK_ID_CURR"] == sk_id].drop(columns=["SK_ID_CURR", "TARGET"], errors="ignore")
        if X.empty:
            return jsonify({"erreur": "Identifiant du client incorrectss."}), 404

        # Get the shap values for the client
        shap_values = explainer.shap_values(X)
        if isinstance(shap_values, list):
            client_shap_values = shap_values[1][0]
        else:
            client_shap_values = shap_values[0]
    
        feature_values = X.iloc[0]

        # Create a DataFrame for local importance
        local_importance_df = pd.DataFrame({
            "feature": feature_names,
            "importance": np.abs(client_shap_values),
            "shap_value": np.round(client_shap_values, 2),
            "value": feature_values.values
        })

        local_importance_df = local_importance_df.sort_values(by="importance", ascending=False)
        local_importance_df_top = local_importance_df.head(10)[["feature", "shap_value", "value"]].to_dict(orient="records")

        # Predictions and probabilities 
        prediction = model.predict(X)
        prediction_proba = model.predict_proba(X)[:, 1]

        # Get the numerical features
        numerical_features = [
            col for col in df.select_dtypes(include=["int64", "float64"])
            .columns.difference(["SK_ID_CURR", "TARGET"])
            if df[col].nunique() > 2
        ]

        # Select the top 3 features based on SHAP values and numerical features
        local_importance_numeric = local_importance_df[local_importance_df["feature"].isin(numerical_features)]
        if prediction[0] == 1:
            selected_features = local_importance_numeric.sort_values(by="shap_value", ascending=False).head(3)
        else:
            selected_features = local_importance_numeric.sort_values(by="shap_value", ascending=True).head(3)

        # Get the selected features, client info, global info and their values
        selected_features_names = selected_features["feature"].tolist()
        client_info = feature_values[selected_features_names].to_dict()
        global_info = df.loc[:, selected_features_names + ["TARGET"]].to_dict(orient="list")

        # Return data for Streamlit
        return jsonify({
            "prediction" : prediction.tolist(),
            "proba_classe_1" : float(prediction_proba[0]),
            "top_10_local_importance" : local_importance_df_top,
            "client_info" : client_info,
            "selected_features" : selected_features_names,
            "global_info" : global_info
        })

