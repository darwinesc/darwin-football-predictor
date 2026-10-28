import streamlit as st
import plotly.graph_objects as go


def donut_chart_goals(probabilidades, linea):
    over = probabilidades[f"Over {linea}"] * 100
    under = probabilidades[f"Under {linea}"] * 100

    fig = go.Figure(
        go.Pie(
            labels=[f"Over {linea}", f"Under {linea}"],
            values=[over, under],
            hole=0.65,
            marker_colors=["#22C55E", "#64748B"],
        )
    )

    fig.update_layout(
        title=f"Probabilidad de goles — línea {linea}",
        showlegend=True,
        height=350,
    )

    st.plotly_chart(fig, use_container_width=True)


def show_all_goal_lines(probabilidades):

    st.subheader("📊 Todas las líneas de goles")

    lineas = [0.5, 1.5, 2.5, 3.5, 4.5]

    cols = st.columns(2)

    for i, linea in enumerate(lineas):
        with cols[i % 2]:
            donut_chart_goals(probabilidades, linea)