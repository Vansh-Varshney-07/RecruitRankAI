import pandas as pd
import plotly.express as px
import streamlit as st


def score_chart(candidates):
    df = pd.DataFrame(candidates)

    if df.empty:
        return

    fig = px.bar(
        df,
        x="score",
        y="name",
        orientation="h",
        color="score",
        color_continuous_scale=[
            [0.0, "#080a12"],
            [0.48, "#ffb199"],
            [1.0, "#6ff3ff"],
        ],
        text=df["score"].map(lambda value: f"{value * 100:.0f}%"),
    )

    fig.update_layout(
        template="plotly_dark",
        height=320,
        margin=dict(l=8, r=8, t=8, b=8),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#f6f7fb"),
        coloraxis_showscale=False,
        xaxis=dict(showgrid=False, zeroline=False, visible=False),
        yaxis=dict(showgrid=False, autorange="reversed"),
    )

    fig.update_traces(
        marker_line_width=0,
        textposition="outside",
        cliponaxis=False,
        hovertemplate="%{y}<br>Score %{x:.2f}<extra></extra>",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )
