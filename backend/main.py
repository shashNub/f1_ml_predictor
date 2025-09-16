import os
import sys
import joblib
import numpy as np
import pandas as pd
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Ensure parent directory is in sys.path to access collect_data
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))
from collect_data import collect_race_results

# === FastAPI App Setup ===
app = FastAPI(title="F1 Predictor API")

# Enable CORS for frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

# Load Trained Models (resolve absolute paths so it works on serverless like Vercel)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
MODELS_DIR = os.path.join(BASE_DIR, 'models')
MODEL_PATH = os.path.join(MODELS_DIR, 'ensemble_model.joblib')
ENCODER_PATH = os.path.join(MODELS_DIR, 'encoder.joblib')

ensemble_model = joblib.load(MODEL_PATH)
encoder = joblib.load(ENCODER_PATH)


# === Request Schema ===
class PredictRequest(BaseModel):
    prix: str

# === Predict Endpoint ===
@app.post("/predict")
def predictTop5(request: PredictRequest):
    prix = request.prix.lower().strip()

    try:
        # Step 1: Collect live features from FastF1 for the specified Grand Prix
        df = collect_race_results(selected_prix=prix, race_day_mode=True)

        # Step 2: Feature Engineering
        df["Quali_vs_Grid"] = df["QualifyingPosition"] - df["GridPosition"]
        df["DriverCircuitExperience"] = df.groupby(["Driver", "Circuit"])["Year"].transform("count")
        df["WeatherType"] = pd.cut(df["Rainfall"], bins=[-0.01, 0.0, 0.5, 100], labels=["Dry", "Light Rain", "Wet"])

        # Step 3: Encode Categorical Features
        categorical_features = ["Driver", "Constructor", "WeatherType", "Circuit", "DriverAggressionStyle"]
        X_cat = encoder.transform(df[categorical_features]).toarray()

        # Numerical features
        numerical_features = ["GridPosition", "AirTemp", "TrackTemp", "Humidity", "Rainfall", "WindSpeed",
                            "Quali_vs_Grid", "DriverCircuitExperience"]
        X_num = df[numerical_features].values
        X = np.hstack([X_num, X_cat])

        # Step 4: Predict using ensemble
        y_preds = np.column_stack([model.predict(X) for model in ensemble_model.values()])
        y_preds_mean = np.mean(y_preds, axis=1)
        y_pred_class = np.clip(np.round(y_preds_mean), 1, 10).astype(int)

        # Step 5: Podium Finishers in sorted order
        df["PredictedPosition"] = y_pred_class
        df_sorted = df.sort_values("PredictedPosition").reset_index(drop=True)

        # Step 6: Format Top 5 Output
        top5 = df_sorted.head(5)
        result = []
        for i, row in top5.iterrows():
            result.append({
                "Position": i+1,
                "driver": row['Driver'],
                "constructor": row['Constructor']
            })
        return {"prix": prix.title(), "predictions": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
