# F1-Predictor

## 🏎️ Overview
Welcome to the F1 Race Predictor Web App — a unique blend of machine learning, Formula 1 passion, and a visually animated frontend. This project is a complete full-stack solution designed to predict the top 5 finishers of any Formula 1 Grand Prix (from 2021 to 2024), combining the power of data with the aesthetics of racing. Powered by FastAPI and React, and styled with styled-components and framer-motion, it offers a fun, immersive experience filled with 🏁 flags, 🏆 trophies, and animated car transitions.

## 🧠 Machine Learning Model
The predictions are driven by a carefully trained ensemble machine learning model, combining XGBoost and Gradient Boosting. It leverages a cleaned and processed dataset built from FastF1 API, including:

Qualifying data
Weather conditions
Driver and constructor performance trends
Circuit

The model outputs a ranked list of likely top 5 finishers. The pipeline is saved using joblib, and preprocessing (e.g., OneHotEncoding) is preserved to ensure accurate future inference.

## ⚙️ Backend (FastAPI)
+ The backend is developed in Python using FastAPI. It serves a single /predict endpoint that:

+ Accepts a Grand Prix name (like "belgian", "monaco", etc.)

+ Internally fetches the relevant data using the FastF1 API

+ Applies preprocessing and feeds the data into the trained model

+ Returns a JSON response of the top 5 drivers with constructors

The API is optimized for fast response and modular design, and will soon be Docker-ready for cloud deployment.

## 🎨 Frontend (React + Framer Motion)
The frontend is built in React using styled-components for styling and framer-motion for smooth animations. Users can enter the Grand Prix name in a form panel, and once submitted, the results are presented in a fun, interactive way:

🥇 Animated Podium Display with 3D-style podiums and tire bases

🏁 Driver Avatars (cartoon-style images or placeholders) standing atop podium blocks

🏆 Trophy for the 1st place winner

🛞 Tire images as podium bases (PNG with transparent background)

✨ Smooth, bounce-in animations for each block and result

4th and 5th place finishers are displayed with a stylish car icon and fade-in animation, adding depth to the experience.

## 🧩 Project Structure
1. /frontend – React app

2. src/components/ – All major UI components (e.g., PodiumDisplay, ResultDisplay)

3. src/assets/ – Driver avatars, tire images, background F1 tracks

4. /backend – FastAPI server

5. main.py – API logic

6. models/ – Trained model, encoder pipeline

7. utils/ – Race data collection & preprocessing code

## 🛠️ How to Run Locally
Backend:
<pre>
cd backend
uvicorn main:app --reload
</pre>

Frontend:
Initially Run this command if there is any problem in npm libraries/modules
<pre>
cd frontend
npm install react-scripts@5.0.1 --save
npm install
</pre>

Don't try to this command as this will break node modules
<pre>
npm audit fix --force
</pre>

Then, run this in terminal
<pre>
npm start
</pre>
Make sure the backend is running on and the frontend sends prediction requests to that address. You can test races like "Belgian", "Australian", or "Monaco".


