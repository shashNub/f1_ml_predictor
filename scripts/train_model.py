import os
import warnings
warnings.filterwarnings('ignore')

# All necessary libraries
import numpy as np
import pandas as pd
from joblib import dump
from xgboost import XGBRegressor
from collect_data import collect_race_results
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import accuracy_score, mean_absolute_error, r2_score

# Collect the data
Grand_Prix = [
  "Abu Dhabi", "Australian", "Austrian", "Azerbaijan", "Bahrain", "Belgian", "Brazilian", "British",
  "Canadian", "Dutch", "Emilia Romagna", "French", "Hungarian", "Italian", "Las Vegas", "Mexican",
  "Miami", "Monaco", "Qatar", "Saudi Arabian", "Singapore", "Spanish", "São Paulo", "United States"
]
all_data = []
for prix_input in Grand_Prix:
    df = collect_race_results(selected_prix=prix_input, race_day_mode=False)
    all_data.append(df)
df = pd.concat(all_data, ignore_index=True)                                                              

# Keep only top 10 racers who completed the race
df = df[(df["Status"] == "Finished") & (df["FinishPosition"] <= 10)]

# Feature Engineering
df["Quali_vs_Grid"] = df["QualifyingPosition"] - df["GridPosition"]
df["DriverCircuitExperience"] = df.groupby(["Driver", "Circuit"])["Year"].transform("count")
df["WeatherType"] = pd.cut(df["Rainfall"], bins=[-0.01, 0.0, 0.5, 100], labels=["Dry", "Light Rain", "Wet"])


# Encode Categorical Features
categorical_features = ["Driver", "Constructor", "WeatherType", "Circuit", "DriverAggressionStyle"]
encoder = OneHotEncoder(handle_unknown="ignore")
X_cat = encoder.fit_transform(df[categorical_features]).toarray()

# Numerical features
numerical_features = ["GridPosition", "AirTemp", "TrackTemp", "Humidity", "Rainfall", "WindSpeed",
                    "Quali_vs_Grid", "DriverCircuitExperience"]
X_num = df[numerical_features].values
X = np.hstack([X_num, X_cat])
y = df['FinishPosition']

# Train and test dataset and Train the model
# Manual Train-Test Split
X_train = X[df["Year"] < 2024]
y_train = y[df["Year"] < 2024]
X_test = X[df["Year"] == 2024]
y_test = y[df["Year"] == 2024]
X_test_df = df[df["Year"] == 2024].copy().reset_index(drop=True)


# Model Initialization
models = {
    "XGBoostRegressor": XGBRegressor(n_estimators=300, learning_rate=0.01, reg_alpha = 0.7, reg_lambda=0.7, random_state=45),
    "GradientBoostingRegressor": GradientBoostingRegressor(n_estimators=300, learning_rate=0.1, random_state=45) 
}

# Model Training and Saving the Model
for name, model in models.items():
    print(f"Training and Evaluating {name}")
    model.fit(X_train, y_train)

os.makedirs("models", exist_ok=True)
dump(models, "models/ensemble_model.joblib")
dump(encoder, "models/encoder.joblib")
print("Saved the model and encoder in 'models/' folder")

# Predictions
y_preds = np.column_stack([model.predict(X_test) for model in models.values()])
y_pred_mean = np.mean(y_preds, axis=1)
y_pred_class = np.clip(np.round(y_pred_mean), 1, 10).astype(int)

# Printing Top 3 Finishing Position Racers
X_test_df["PredictedFinish"] = y_pred_class
X_test_df_sorted = X_test_df.sort_values("PredictedFinish").reset_index(drop=True)
print("\n Predicted Podium Finishers : ")
places = ["🥇 1st Place", "🥈 2nd Place", "🥉 3rd Place", "🏅 4th Place", "🏅 5th Place"]
for i in range(min(5, len(X_test_df_sorted))):
    driver = X_test_df_sorted.iloc[i]["Driver"]
    constructor = X_test_df_sorted.iloc[i]["Constructor"]
    circuit = X_test_df_sorted.iloc[i]["Circuit"]
    grid = X_test_df_sorted.iloc[i]["GridPosition"]
    actual = X_test_df_sorted.iloc[i]["FinishPosition"]
    print(f"{places[i]}. 🏎️  Driver: {driver:<15} | Team: {constructor:<15} | Circuit: {circuit:<12} | Grid: {grid:<2} | Actual: {actual} |")

# Evaluation (Accuracy Scores)
top1 = accuracy_score(y_test, y_pred_class)
mae = mean_absolute_error(y_test, y_pred_class)
r2 = r2_score(y_test, y_pred_class)

print(f"Top-1 accuracy: {top1:.4f}")
print(f"Mean Absolute Error: {mae:.4f}")
print(f"R2 score: {r2:.4f}")
    