from flask import Flask, request, jsonify
import joblib
import shap
import numpy as np 
import pandas as pd
import os


app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(BASE_DIR, "..", "models", "LGBMClassifier_model.joblib")
model = joblib.load(model_path)

df_path = os.path.join(BASE_DIR, "..", "data", "dashboard", "df_sample.csv")
df = pd.read_csv(df_path, sep=";", encoding="utf-8")

clf = model.named_steps["clf"]
feature_names = df.drop(columns=["TARGET", "SK_ID_CURR"], errors="ignore").columns.tolist()

importances = clf.feature_importances_
importances_df = pd.DataFrame({
  "feature": feature_names,
  "importance": importances
})
importances_df = importances_df.sort_values(by="importance", ascending=False)
importances_df_top = importances_df.head(10)[["feature", "importance"]].to_dict(orient="records")

explainer = shap.TreeExplainer(clf)

@app.route("/")
def home():
  return "Bienvenue sur l'API."


@app.route("/predict", methods=["POST"])
def predict():
  # Récupération des données envoyées en JSON
  data = request.get_json()
  sk_id = data["SK_ID_CURR"]
  
  sample = df[df["SK_ID_CURR"] == sk_id].copy()
  if sample.empty:
    return jsonify({"erreur": "Identifiant du client incorrectss."}), 404
  
  X = sample.copy()
  X.drop(columns=["SK_ID_CURR", "TARGET"], inplace=True)
  
  shap_values = explainer.shap_values(X)
  
  if isinstance(shap_values, list):
    client_shap_values = shap_values[1][0]
  else:
    client_shap_values = shap_values[0]
    
  feature_values = X.iloc[0].values
    
  local_importance_df = pd.DataFrame({
    "feature": feature_names,
    "importance": np.abs(client_shap_values),
    "shap_value": np.round(client_shap_values, 2),
    "value": feature_values
  })
  local_importance_df = local_importance_df.sort_values(by="importance", ascending=False)
  local_importance_df_top = local_importance_df.head(10)[["feature", "shap_value", "value"]].to_dict(orient="records")
  
  prediction = model.predict(X)
  prediction_proba = model.predict_proba(X)[:, 1]
  
  return jsonify({
    "prediction" : prediction.tolist(),
    "proba_classe_1" : float(prediction_proba[0]),
    "top_10_feature_importance" : importances_df_top,
    "top_10_local_importance" : local_importance_df_top,
    })

if __name__ == "__main__":
  app.run(debug=True, port=5000)