# Backend API for the ExtraaLearn lead-conversion model
import joblib
import pandas as pd
from flask import Flask, request, jsonify

app = Flask("ExtraaLearn Lead Conversion Predictor")

# Load the saved pipeline (preprocessing + model) once when the server starts
model = joblib.load("extraalearn_model_v1_0.joblib")

FEATURES = [
    "age", "current_occupation", "first_interaction", "profile_completed",
    "website_visits", "time_spent_on_website", "page_views_per_visit", "last_activity",
    "print_media_type1", "print_media_type2", "digital_media", "educational_channels", "referral",
]

@app.get("/")
def home():
    return "Welcome to the ExtraaLearn Lead Conversion Prediction API!"

@app.post("/v1/lead")
def predict_single_lead():
    """Predict for ONE lead. Expects a JSON object with the feature names above."""
    lead = request.get_json()
    missing = [f for f in FEATURES if f not in lead]
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400
    input_df = pd.DataFrame([lead])[FEATURES]
    pred = int(model.predict(input_df)[0])
    prob = float(model.predict_proba(input_df)[0][1])
    return jsonify({
        "prediction": "Likely to convert" if pred == 1 else "Unlikely to convert",
        "conversion_probability": round(prob, 4),
    })

@app.post("/v1/leadbatch")
def predict_batch():
    """Predict for MANY leads. Expects a CSV file uploaded under the key 'file'."""
    file = request.files["file"]
    input_df = pd.read_csv(file)
    ids = input_df["ID"].tolist() if "ID" in input_df.columns else list(range(len(input_df)))
    preds = model.predict(input_df[FEATURES]).tolist()
    return jsonify(dict(zip(map(str, ids), preds)))

if __name__ == "__main__":
    app.run(debug=True)
