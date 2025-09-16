kannda liver

import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
from joblib import load
from collect_data import collect_race_results

# Loading ensemble model and encoder
ensemble_model = load("models/ensemble_model.joblib")
encoder = load("models/encoder.joblib")

selected_prix = input("Enter today's prix (e.g. Austrian, Belgian): ").strip()
print(f"📡 Collecting live race data features...")
df = collect_race_results(selected_prix=selected_prix, race_day_mode=True)

if df.empty:
    exit("⛔ Prediction aborted. No race today.")


# Feature Engineering
df["Quali_vs_Grid"] = df["QualifyingPosition"] - df["GridPosition"]
df["DriverCircuitExperience"] = df.groupby(["Driver", "Circuit"])["Year"].transform("count")
df["WeatherType"] = pd.cut(df["Rainfall"], bins=[-0.01, 0.0, 0.5, 100], labels=["Dry", "Light Rain", "Wet"])

# Encode Categorical Features
categorical_features = ["Driver", "Constructor", "WeatherType", "Circuit", "DriverAggressionStyle"]
X_cat = encoder.transform(df[categorical_features]).toarray()

# Numerical features
numerical_features = ["GridPosition", "AirTemp", "TrackTemp", "Humidity", "Rainfall", "WindSpeed",
                    "Quali_vs_Grid", "DriverCircuitExperience"]
X_num = df[numerical_features].values
X = np.hstack([X_num, X_cat])

# Predict using ensemble
y_preds = np.column_stack([model.predict(X) for model in ensemble_model.values()])
y_preds_mean = np.mean(y_preds, axis=1)
y_pred_class = np.clip(np.round(y_preds_mean), 1, 10).astype(int)

# Display Podium Finishers
df["PredictedPosition"] = y_pred_class
df_sorted = df.sort_values("PredictedPosition").reset_index(drop=True)

print("\n🏁 Predicted Podium Finishers for Today's Race:\n")
places = ["🥇 1st Place", "🥈 2nd Place", "🥉 3rd Place", "🏅 4th Place", "🏅 5th Place"]

for i in range(min(5, len(df_sorted))):
    driver = df_sorted.iloc[i]["Driver"]
    constructor = df_sorted.iloc[i]["Constructor"]
    circuit = df_sorted.iloc[i]["Circuit"]
    grid = df_sorted.iloc[i]["GridPosition"]
    print(f"{places[i]}. 🏎️  Driver: {driver:<15} | Team: {constructor:<15} | Circuit: {circuit:<12} | Grid: {grid:<2} |")

