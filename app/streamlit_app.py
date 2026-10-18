import streamlit as st
import pandas as pd
from football_predictor.data.loader import load_data
from football_predictor.features.builder import build_features
from football_predictor.model.trainer import train_model


st.title("⚽ Football Match Predictor")

df = load_data()
model_df, team_stats = build_features(df)
model, accuracy = train_model(model_df)

st.write(f"Model accuracy: {round(accuracy*100,2)}%")

teams = list(team_stats.keys())

home_team = st.selectbox("Home Team", teams)
away_team = st.selectbox("Away Team", teams)

if st.button("Predict"):

    input_data = pd.DataFrame([{
        "home_attack": team_stats[home_team]["attack"],
        "home_defense": team_stats[home_team]["defense"],
        "away_attack": team_stats[away_team]["attack"],
        "away_defense": team_stats[away_team]["defense"],
    }])

    prediction = model.predict(input_data)[0]
    probabilities = model.predict_proba(input_data)[0]

    st.subheader("Prediction")
    st.write(f"Result: **{prediction}**")
    st.write("H = Home | D = Draw | A = Away")

    prob_df = pd.DataFrame({
        "Outcome": model.classes_,
        "Probability": probabilities
    })

    st.bar_chart(prob_df.set_index("Outcome"))
