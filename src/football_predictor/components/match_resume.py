import streamlit as st

def show_match_resume(home_team, away_team, home_crest, away_crest, prob_home, prob_draw, prob_away):

    st.subheader("⚽ Predicción del Partido")

    col1, col2, col3 = st.columns([2, 1, 2])

    with col1:
        st.image(home_crest, width=90)
        st.markdown(f"**{home_team}**")
        st.metric("Victoria local", f"{prob_home:.1f}%")

    with col2:
        st.markdown("## VS")
        st.metric("Empate", f"{prob_draw:.1f}%")

    with col3:
        st.image(away_crest, width=90)
        st.markdown(f"**{away_team}**")
        st.metric("Victoria visitante", f"{prob_away:.1f}%")