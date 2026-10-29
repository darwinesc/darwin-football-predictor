import pandas as pd
import streamlit as st

def get_h2h(df, team1, team2):
    ''' Return all match between two teams '''

    required = {
        "HomeTeam",
        "AwayTeam",
        "FTHG",
        "FTAG",
    }
    
    missing = required - set(df.columns)
    
    if missing:
        raise ValueError(
            f"Faltan columnas obligatorias: {sorted(missing)}"
        )
    data = df.copy()

    data["Date"] = pd.to_datetime(data["Date"], dayfirst=True, errors="coerce")

    data["FTHG"] = pd.to_numeric(data["FTHG"], errors="coerce")
    data["FTAG"] = pd.to_numeric(data["FTAG"], errors="coerce")

    data = data.dropna(subset=["Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG"])

    h2h = data.query(
                        "(HomeTeam == @team1 and AwayTeam == @team2) or "
                        "(HomeTeam == @team2 and AwayTeam == @team1)"
                    )

    # Sort from newest to oldest match
    h2h = h2h.sort_values("Date", ascending=False)
    
    return h2h


def show_h2h(df, team1, team2):

    st.subheader(f"⚔️ H2H: {team1} vs {team2}")

    h2h = get_h2h(df, team1, team2)

    if h2h.empty:
        st.info("No existen entrentamientos cara a cara entre estos equipos")
        return

    # Resultados desde la perspectiva del equipo1
    team1_home = h2h["HomeTeam"] == team1

    goals1 = (
        h2h["FTHG"].where(team1_home, h2h["FTAG"])
    )
    goals2 = (
        h2h["FTAG"].where(team1_home, h2h["FTHG"])
    )

    total = len(h2h)
    wins = int((goals1 > goals2).sum())
    draws = int((goals1 == goals2).sum())
    losses = int((goals1 == goals2).sum())

    total_goals = goals1 + goals2
    over15 = float((total_goals >= 2).mean() * 100)
    over25 = float((total_goals >= 3).mean() * 100)
    btts = float(
        ((h2h["FTHG"] > 0) & (h2h["FTAG"] > 0)).mean() * 100
    )

    # Métricas principales
    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Partidos", total)
    c2.metric(f"Victorias {team1}", wins)
    c3.metric("Empates", draws)
    c4.metric(f"Victorias {team2}", losses)

    g1, g2, g3, g4 = st.columns(4)

    g1.metric("Goles por partido", f"{total_goals.mean():.2f}")
    g2.metric("Over 1.5", f"{over15:.1f}%")
    g3.metric("Over 2.5", f"{over25:.1f}%")
    g4.metric("BTTS", f"{btts:.1f}%")

    st.markdown("#### 📅 Historial de enfrentamientos")

    tabla = h2h[
        ["Date", "HomeTeam", "FTHG", "FTAG", "AwayTeam"]
    ].copy()

    tabla.columns = [
        "Fecha", "Local", "Goles local",
        "Goles visitante", "Visitante"
    ]

    tabla["Fecha"] = tabla["Fecha"].dt.strftime("%d/%m/%Y")

    st.dataframe(
        tabla,
        use_container_width=True,
        hide_index=True,
    )