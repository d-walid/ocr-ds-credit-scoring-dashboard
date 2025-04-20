from scripts.app import app, model, df


def test_predict_endpoint():
    client = app.test_client()
    sample_client_id = df["SK_ID_CURR"].iloc[0]
    response = client.post("/predict", json={"SK_ID_CURR": int(sample_client_id)})
    data = response.get_json()
    assert response.status_code == 200
    assert "prediction" in data
    assert "proba_classe_1" in data
    assert "top_10_feature_importance" in data
    assert "top_10_local_importance" in data
    
    
def test_model_prediction():
    sample_client_id = df["SK_ID_CURR"].iloc[0]
    sample = df[df["SK_ID_CURR"] == sample_client_id].copy()
    assert not sample.empty
    
    X = sample.drop(columns=["SK_ID_CURR", "TARGET"], errors="ignore")
    X_preprocessed = model[:-1].transform(X)
    
    prediction = model.predict(X_preprocessed)
    prediction_proba = model.predict_proba(X_preprocessed)
    
    assert prediction.shape[0] == 1
    assert 0 <= prediction_proba[0][1] <= 1