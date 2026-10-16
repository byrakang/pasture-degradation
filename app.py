import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from analysis import FEATURE_IMPORTANCE, Inputs, assess, build_insights, build_report_csv, load_model
from i18n import LANGUAGES, TRANSLATIONS
from ui import components as ui
from ui.styles import GLOBAL_CSS

st.set_page_config(
    page_title="Pasture Risk AI · Pasture Degradation Risk Prediction",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed",
)
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

SLIDERS = [
    # key, label key, min, max, default
    ("precip", "lbl_precip", 0.0, 600.0, 250.0),
    ("temp", "lbl_temp", -30.0, 45.0, 1.5),
    ("pasture", "lbl_pasture", 100.0, 10000.0, 3738.0),
    ("count", "lbl_count", 100.0, 10000.0, 2679.0),
    ("loss", "lbl_loss", 0.0, 2000.0, 120.0),
]
CHART_FONT = dict(family="Inter, sans-serif", color="#475569", size=12)
PLOTLY_CONFIG = {"displayModeBar": False, "responsive": True}


@st.cache_resource
def get_model():
    return load_model()


def transparent_layout(fig: go.Figure, height: int, **kwargs) -> go.Figure:
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=CHART_FONT,
        **kwargs,
    )
    return fig


# Sliders render further down the page, but the hero needs their values first.
# Streamlit stores widget values in session_state before each rerun, so read them here.
inputs = Inputs(**{key: st.session_state.get(key, default) for key, _, _, _, default in SLIDERS})

# ---------- Navigation ----------
ui.html('<div id="top"></div>')
with st.container(key="glass_nav"):
    c_brand, c_links, c_lang, c_about = st.columns([3, 5, 1.6, 1.4], vertical_alignment="center")
    with c_lang:
        lang = st.segmented_control(
            "Language",
            options=list(LANGUAGES),
            format_func=LANGUAGES.get,
            default="Монгол",
            key="lang_switch",
            label_visibility="collapsed",
        ) or "Монгол"
    t = TRANSLATIONS[lang]
    with c_brand:
        ui.html(ui.brand(t))
    with c_links:
        ui.html(ui.nav_links(t))
    with c_about:
        open_about = st.button(t["nav_about"], key="about_btn", icon=":material/public:")


@st.dialog("UNCCD COP-17", width="large")
def show_cop_info():
    ui.html(ui.cop_dialog_body(t))


if open_about:
    show_cop_info()

result = assess(inputs, get_model())
critical, positive, recs = build_insights(inputs, t)

# ---------- Hero ----------
hero_left, hero_right = st.columns([1.15, 1], gap="large", vertical_alignment="center")
with hero_left:
    ui.html(ui.hero_copy(t))
with hero_right:
    ui.html(ui.hero_preview(t, result))

# ---------- Simulator ----------
ui.html(ui.section_head("simulator", "sliders", t["sim_eyebrow"], t["sim_title"], t["sim_desc"]))
with st.container(key="card_simulator"):
    rows = [SLIDERS[:3], SLIDERS[3:]]
    for row in rows:
        cols = st.columns(3, gap="large")
        for col, (key, label_key, lo, hi, default) in zip(cols, row):
            with col:
                st.slider(t[label_key], lo, hi, default, key=key)
        if len(row) < 3:
            with cols[-1]:
                ui.html(ui.density_readout(t, inputs))

# ---------- Insights ----------
ui.html(ui.section_head("insights", "bar-chart", t["insights_eyebrow"], t["insights_title"], t["insights_desc"]))
ui.html(ui.kpi_grid(t, inputs))
st.write("")

chart_left, chart_right = st.columns(2, gap="medium")
with chart_left:
    with st.container(key="card_donut"):
        ui.html(ui.card_head("target", "", t["donut_title"], t["donut_subtitle"]))
        donut = go.Figure(
            go.Pie(
                labels=list(t["prob_labels"]),
                values=[result.prob_high, result.prob_med, result.prob_low],
                hole=0.68,
                sort=False,
                marker=dict(colors=["#EF4444", "#F59E0B", "#10B981"], line=dict(color="#FFFFFF", width=3)),
                textinfo="none",
                hovertemplate="%{label}: %{value}%<extra></extra>",
            )
        )
        transparent_layout(
            donut,
            280,
            margin=dict(l=10, r=10, t=10, b=10),
            legend=dict(orientation="h", y=-0.08, x=0.5, xanchor="center"),
            annotations=[
                dict(
                    text=f"<b style='font-size:26px;color:{result.color}'>{t['risk_names'][result.level]}</b>"
                    f"<br><span style='font-size:12px'>{result.score}/100</span>",
                    showarrow=False,
                    x=0.5,
                    y=0.5,
                )
            ],
        )
        st.plotly_chart(donut, width="stretch", config=PLOTLY_CONFIG)

with chart_right:
    with st.container(key="card_radar"):
        ui.html(ui.card_head("activity", "green", t["radar_title"], t["radar_subtitle"]))
        radar = go.Figure(
            go.Scatterpolar(
                r=[
                    min(inputs.precip / 600.0, 1.0),
                    min((inputs.temp + 30) / 75.0, 1.0),
                    min(inputs.pasture / 10000.0, 1.0),
                    min(inputs.count / 10000.0, 1.0),
                    min(inputs.density / 3.0, 1.0),
                ],
                theta=t["categories"],
                fill="toself",
                fillcolor="rgba(2, 132, 199, 0.18)",
                line=dict(color="#0284C7", width=2.5),
                marker=dict(size=7, color="#0284C7"),
            )
        )
        transparent_layout(
            radar,
            280,
            showlegend=False,
            margin=dict(l=50, r=50, t=20, b=20),
            polar=dict(
                bgcolor="rgba(0,0,0,0)",
                radialaxis=dict(visible=True, range=[0, 1], gridcolor="#E2E8F0", linecolor="#E2E8F0", tickfont=dict(size=10)),
                angularaxis=dict(gridcolor="#E2E8F0", linecolor="#E2E8F0"),
            ),
        )
        st.plotly_chart(radar, width="stretch", config=PLOTLY_CONFIG)

st.write("")
summary_col, recs_col = st.columns(2, gap="medium")
with summary_col:
    ui.html(ui.summary_card(t, result, critical, positive))
with recs_col:
    with st.container(key="card_recs"):
        ui.html(ui.recommendations_card(t, recs))
        st.download_button(
            t["export_btn"],
            data=build_report_csv(inputs, result, recs, t),
            file_name="pasture_risk_report.csv",
            mime="text/csv",
            key="export_btn",
            icon=":material/download:",
            width="stretch",
        )

st.write("")
with st.container(key="card_importance"):
    ui.html(ui.card_head("bar-chart", "", t["feature_title"], t["feature_subtitle"]))
    importance = sorted(FEATURE_IMPORTANCE.items(), key=lambda item: item[1])
    bars = go.Figure(
        go.Bar(
            x=[value for _, value in importance],
            y=[t["feature_labels"][key] for key, _ in importance],
            orientation="h",
            marker=dict(color=[value for _, value in importance], colorscale=[[0, "#BAE6FD"], [1, "#0284C7"]]),
            text=[f"{value:.1f}%" for _, value in importance],
            textposition="outside",
            hovertemplate="%{y}: %{x:.1f}%<extra></extra>",
        )
    )
    transparent_layout(
        bars,
        320,
        margin=dict(l=10, r=30, t=10, b=30),
        xaxis=dict(title=t["importance_axis"], gridcolor="#EEF2F7", zeroline=False, range=[0, 56]),
        yaxis=dict(gridcolor="rgba(0,0,0,0)"),
        bargap=0.35,
    )
    st.plotly_chart(bars, width="stretch", config=PLOTLY_CONFIG)

# ---------- Mission ----------
ui.html(ui.section_head("mission", "target", t["mission_eyebrow"], t["mission_title"], t["mission_desc"]))
ui.html(ui.mission_section(t))

# ---------- Dataset ----------
ui.html(ui.section_head("dataset", "database", t["dataset_eyebrow"], t["dataset_title"], t["dataset_caption"]))
with st.container(key="card_dataset"):
    spec = [
        ("precipitation", t["unit_mm"], t["role_input"]),
        ("temperature", "°C", t["role_input"]),
        ("pasture_area", t["unit_area"], t["role_input"]),
        ("livestock_count", t["unit_thousand"], t["role_input"]),
        ("livestock_loss", t["unit_thousand"], t["role_input"]),
        ("livestock_density", t["unit_density"], t["role_derived"]),
    ]
    st.dataframe(
        pd.DataFrame(
            [
                {
                    t["col_feature"]: t["feature_labels"][key],
                    t["col_unit"]: unit,
                    t["col_role"]: role,
                    t["col_desc"]: t["dataset_descs"][key],
                }
                for key, unit, role in spec
            ]
        ),
        hide_index=True,
        width="stretch",
    )
    uploaded_file = st.file_uploader(t["upload_label"], type=["csv", "xlsx"])
    if uploaded_file is not None:
        try:
            reader = pd.read_csv if uploaded_file.name.lower().endswith(".csv") else pd.read_excel
            st.caption(t["upload_preview"])
            st.dataframe(reader(uploaded_file).head(50), width="stretch")
        except Exception:
            st.error(t["upload_error"])

# ---------- Footer ----------
ui.html(ui.footer(t))
