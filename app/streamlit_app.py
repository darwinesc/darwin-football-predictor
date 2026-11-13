import streamlit as st
import pandas as pd
from football_predictor.data.loader import load_data, load_csv
from football_predictor.features.builder import build_features
from football_predictor.model.trainer import train_model
from football_predictor.model.goal_prob import get_goal_prob
from football_predictor.components.goal_chart import show_all_goal_lines
from football_predictor.components.h2h import show_h2h
from football_predictor.components.match_resume import show_match_resume
from football_predictor.components.logos import merge_team_logos

st.title("⚽ Football Match Predictor")

df = load_data("E0.csv")
df_logo = load_csv("clubs_badges.csv")
merge_df = merge_team_logos(df, df_logo)
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
    match_df_log = merge_df[(merge_df["HomeTeam"] == home_team) & (merge_df["AwayTeam"] == away_team)]
    #st.dataframe(match_df_log[["HomeTeam", "AwayTeam", "HomeLogo", "AwayLogo"]])
    prediction = model.predict(input_data)[0]
    probabilities = model.predict_proba(input_data)[0]

    prob_away, prob_draw, prob_home = probabilities * 100

    print(type(probabilities))

    st.subheader("Prediction")

    if not match_df_log.empty:

        show_match_resume(
            home_team=match_df_log['HomeTeam'].iloc[0],
            away_team=match_df_log['AwayTeam'].iloc[0],
            home_crest=match_df_log['HomeLogo'].iloc[0],
            away_crest=match_df_log['AwayLogo'].iloc[0],
            prob_home=prob_home,
            prob_draw=prob_draw,
            prob_away=prob_away
        )
    else:
        st.warning("No se encontró el partido seleccionado")

    st.write(f"Result: **{prediction}**")
    st.write("H = Home | D = Draw | A = Away")

    prob_df = pd.DataFrame({
        "Outcome": model.classes_,
        "Probability": probabilities
    })

    st.bar_chart(prob_df.set_index("Outcome"))

    # Calculate goal prob
    probabilidades = get_goal_prob(input_data["home_attack"], input_data["away_attack"])

    #Show Donut Chart goals
    show_all_goal_lines(probabilidades)

    with st.expander("⚔️ Historial H2H", expanded=True):
        show_h2h(df, home_team, away_team)


    