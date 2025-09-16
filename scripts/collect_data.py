import os
import fastf1
import datetime
import pandas as pd
from fastf1 import get_session

# Configure FastF1 cache. On serverless (e.g., Vercel), only /tmp is writable.
cache_dir_env = os.getenv('FASTF1_CACHE_DIR')
cache_dir = cache_dir_env or ('/tmp/f1_cache' if os.name != 'nt' else 'f1_cache')
if not os.path.exists(cache_dir):
    os.makedirs(cache_dir, exist_ok=True)
fastf1.Cache.enable_cache(cache_dir)

driver_name = {
    "VER": "Max Verstappen", "HAM": "Lewis Hamilton", "PER": "Sergio Perez", 
    "SAI": "Carlos Sainz", "RUS": "George Russell", "ALO": "Fernando Alonso",
    "LEC": "Charles Leclerc", "OCO": "Esteban Ocon", "VET": "Sebastian Vettel",
    "GAS": "Pierre Gasly", "ALB": "Alexander Albon", "STR": "Lance Stroll",
    "NOR": "Lando Norris", "TSU": "Yuki Tsunoda", "ZHO": "Guanyu Zhou",
    "RIC": "Daniel Ricciardo",  "MAG": "Kevin Magnussen", "MSC": "Mick Schumacher",
    "LAT": "Nicholas Latifi", "BOT": "Valtteri Bottas", "HUL": "Nico Hulkenberg",
    "DEV": "Nyck de Vries", "DRU": "Jack Doohan",  "PIA": "Oscar Piastri",
    "SAR": "Logan Sargeant", "GIO": "Antonio Giovinazzi", "MAZ": "Nikita Mazepin",
    "RAI": "Kimi Räikkönen"
}

downforce_map = {
    "Red Bull": "Low",  
    "Ferrari": "High",
    "Mercedes": "Medium",
    "McLaren": "Medium",
    "Williams": "Low",
    "Haas": "High"
}

aggression_style_map = {
    "Max Verstappen": "Aggressive", "Lewis Hamilton": "Balanced", "Charles Leclerc": "Aggressive",
    "Carlos Sainz": "Balanced", "George Russell": "Balanced", "Lando Norris": "Balanced",
    "Fernando Alonso": "Aggressive", "Sergio Perez": "Defensive", "Oscar Piastri": "Balanced",
    "Esteban Ocon": "Aggressive", "Pierre Gasly": "Balanced", "Yuki Tsunoda": "Aggressive",
    "Valtteri Bottas": "Defensive", "Alexander Albon": "Balanced", "Kevin Magnussen": "Aggressive",
    "Daniel Ricciardo": "Defensive", "Nico Hulkenberg": "Balanced", "Guanyu Zhou": "Defensive",
    "Lance Stroll": "Defensive", "Logan Sargeant": "Defensive", "Mick Schumacher": "Balanced",
    "Nicholas Latifi": "Defensive", "Nyck de Vries": "Balanced", "Jack Doohan": "Balanced",
    "Antonio Giovinazzi": "Balanced", "Nikita Mazepin": "Aggressive", "Kimi Räikkönen": "Defensive"
}

def collect_race_results(selected_prix=None, race_day_mode = False):
    all_data = []
    start_year = 2021
    end_year = 2024

    if race_day_mode:
        today = datetime.date.today()
        start_year = end_year = today.year
        selected_prix = selected_prix

    for year in range(start_year, end_year+1):
        try:
            schedule = fastf1.get_event_schedule(year)
            if schedule is None or schedule.empty:
                exit(f"❌ Could not load schedule for year: {year}")
            races = schedule[schedule['EventFormat'].str.contains("sprint", case=False) | schedule['EventFormat'].str.contains("conventional", case=False)]

            if race_day_mode:
                prix_matches = races[races['EventName'].str.lower().str.contains(selected_prix.lower())]
                if prix_matches.empty:
                    exit(f"❌ No Grand Prix found matching '{selected_prix}' in {year}.")
                
                # Filter for races already completed (i.e., date < today)
                past_races = prix_matches[prix_matches['EventDate'].dt.date <= today]
                if past_races.empty:
                    exit(f"📅 The {selected_prix.title()} GP has not occurred yet in {year}.")

                # Get the most recent completed GP
                latest_race = past_races.sort_values(by='EventDate', ascending=False).iloc[0:1]
                races = latest_race

            for _, event in races.iterrows():
                circuit_name = event['EventName']
                rnd = int(event['RoundNumber'])
                if selected_prix.lower() not in circuit_name.lower():
                    continue
                try:
                    race = get_session(year, rnd, 'R')
                    race.load(telemetry=False, weather=True, messages=False)

                    quali = get_session(year, rnd, 'Q')
                    quali.load(telemetry=False, weather=False, messages=False)
                    
                    df = race.results.copy()
                    df["Year"] = year
                    df["Round"] = rnd
                    df["Circuit"] = race.event["EventName"]
                    df["Driver"] = df["Abbreviation"]
                    df["Constructor"] = df["TeamName"]
                    df["CarDownforcePreference"] = df["Constructor"].map(downforce_map).fillna("Medium")
                    df["GridPosition"] = pd.to_numeric(df["GridPosition"], errors='coerce').fillna(0).astype(int)
                    df["FinishPosition"] = pd.to_numeric(df["Position"], errors='coerce').fillna(0).astype(int)
                    df["Status"] = df["Status"]

                    # Qualifying Position
                    quali_df = quali.results.copy()
                    qualify_df = quali_df[["Abbreviation", "Position"]].rename(
                        columns={"Abbreviation": "Driver", "Position": "QualifyingPosition"}
                    )
                    qualify_df["QualifyingPosition"] = pd.to_numeric(qualify_df["QualifyingPosition"], errors="coerce").fillna(0).astype(int)

                    merged = pd.merge(df, qualify_df, on="Driver", how="left")
                    merged["Driver"] = merged["Driver"].map(driver_name).fillna(merged["Driver"])
                    merged["DriverAggressionStyle"] = merged["Driver"].map(aggression_style_map).fillna("Balanced")

                    # Weather (average over all race)
                    weather = race.weather_data
                    weather_cols =["AirTemp", "TrackTemp", "Humidity", "Rainfall", "WindSpeed"]
                    available_cols = [col for col in weather_cols if col in weather.columns]
                    avg_weather = weather[available_cols].mean()

                    for col in avg_weather.index:
                        merged[col] = avg_weather[col]
                    
                    final_cols  = ["Year", "Round", "Circuit", "Driver", "Constructor",
                                    "CarDownforcePreference", "DriverAggressionStyle", 
                                    "GridPosition", "QualifyingPosition", "FinishPosition", "Status",
                                    "AirTemp", "TrackTemp", "Humidity", "Rainfall", "WindSpeed"]
                    merged = merged[final_cols]
                    all_data.append(merged)
                    print(f"Collected data for year: {year} and Round: {rnd}")
                except Exception as e:
                    print(f"Skipped for year: {year} and Round: {rnd} - {e}")
        except Exception as e:
            print(f"Failed to load schedule for year: {year} - {e}")
    
    if not all_data:
        print("❌ No data was collected for the selected Grand Prix.")
        return pd.DataFrame()

    df = pd.concat(all_data, ignore_index=True)
    driver_gp_perf = df.groupby(['Driver', 'Circuit'])['FinishPosition'].mean().reset_index()
    driver_gp_perf.rename(columns={'FinishPosition': 'DriverGPForm'}, inplace=True)
    df = pd.merge(df, driver_gp_perf, on=['Driver', 'Circuit'], how='left')

    return df
