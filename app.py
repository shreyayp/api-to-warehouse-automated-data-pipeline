from __future__ import annotations

import sys
from pathlib import Path
from datetime import date

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

st.set_page_config(
    page_title="WeatherScope India | Weather Intelligence",
    page_icon="🌦️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Theme ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500;600&family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');
:root {
  --bg:#080D18; --surface:#101A2B; --surface2:#15243A; --surface3:#1B2D46;
  --line:#2B405C; --text:#F4F7FF; --muted:#B6C5D9; --soft:#8FA4BE;
  --cyan:#53E0D0; --blue:#8BA7FF; --lime:#B9F36B; --pink:#FF79B8;
}
html, body, [class*="css"] {font-family:'DM Sans',sans-serif;}
.stApp {background:radial-gradient(ellipse at 78% 0%,#23456b55,transparent 34%),linear-gradient(145deg,#080D18,#0A1220 65%,#0B1422);color:var(--text)}
[data-testid="stHeader"]{background:rgba(8,13,24,.92)}
[data-testid="stSidebar"]{background:#0C1626;border-right:1px solid #263B56}
[data-testid="stSidebar"] *{color:#E7EFFB}
.block-container{padding-top:1.8rem;padding-bottom:3rem;max-width:1500px}
h1,h2,h3,h4{font-family:'Space Grotesk',sans-serif!important;color:#F4F7FF!important;letter-spacing:-.45px}
h1{font-weight:700!important} h2,h3{font-weight:650!important}
p,li,.stMarkdown,.stCaptionContainer{color:#C2D0E2}
label,[data-testid="stWidgetLabel"] p{color:#D3DEEC!important;font-weight:600!important;font-size:12px!important;letter-spacing:.25px}
[data-testid="stCaptionContainer"] p{color:#9FB1C8!important}
.smallcaps{font:600 10px 'DM Mono',monospace;letter-spacing:1.8px;color:#53E0D0;text-transform:uppercase}
.hero-title{font:700 clamp(32px,4vw,48px) 'Space Grotesk',sans-serif;color:#F7FAFF;letter-spacing:-1.8px;margin:3px 0 5px}
.hero-sub{color:#B8C8DC;font-size:14px;margin-bottom:18px;line-height:1.6}
.panel-title{font:700 14px 'Space Grotesk',sans-serif;color:#F2F6FF;margin-bottom:5px}
.panel-sub{font:11px 'DM Mono',monospace;color:#A9BCD3;letter-spacing:.1px}
.pill{display:inline-block;padding:6px 10px;border-radius:20px;border:1px solid #27665F;background:#102F32;color:#70F0D9;font:600 10px 'DM Mono',monospace}
/* Metric cards */
div[data-testid="stMetric"]{background:linear-gradient(145deg,#172942,#101B2C);border:1px solid #2D4564;border-radius:16px;padding:17px 19px;box-shadow:0 12px 30px #0003}
div[data-testid="stMetric"] label{color:#B9C9DD!important;font-size:11px!important;font-weight:700!important;letter-spacing:.6px}
div[data-testid="stMetric"] [data-testid="stMetricValue"]{color:#53E0D0!important;font-family:'Space Grotesk',sans-serif;font-weight:700}
div[data-testid="stMetric"] [data-testid="stMetricDelta"]{color:#B9F36B!important}
/* Inputs and filters */
div[data-baseweb="select"]>div,div[data-baseweb="input"]>div,[data-testid="stDateInput"] input{background:#142238!important;border:1px solid #38516F!important;color:#F4F7FF!important;border-radius:9px!important}
div[data-baseweb="select"] input{color:#F4F7FF!important}
div[data-baseweb="tag"]{background:#174A4B!important;border:1px solid #2E8D83!important;border-radius:7px!important;box-shadow:none!important}
div[data-baseweb="tag"] *{color:#E9FFFA!important}
div[data-baseweb="tag"] svg{fill:#B9F36B!important}
[data-testid="stMultiSelect"] [data-baseweb="tag"]{background:#174A4B!important}
[data-testid="stDateInput"] input{background:#142238!important;color:#F4F7FF!important;border:1px solid #38516F!important;border-radius:10px!important;box-shadow:none!important}
[data-testid="stSlider"] [role="slider"]{background:#53E0D0!important;border:2px solid #53E0D0!important}
[data-testid="stSlider"] [data-testid="stTickBar"]{background:#38516F!important}
[data-testid="stDateInput"] input{color:#F4F7FF!important;opacity:1!important}
[data-testid="stSlider"] [data-baseweb="slider"] div[role="slider"]{background:#53E0D0!important;border-color:#53E0D0!important;box-shadow:0 0 0 4px #53E0D022!important}
[data-testid="stSlider"] [data-baseweb="slider"] div[data-testid="stSliderTrack"]{background:#53E0D0!important}
[data-testid="stSlider"] [data-baseweb="slider"] div[data-testid="stSliderTrack"]:before{background:#53E0D0!important}
[data-testid="stSlider"] [data-testid="stTickBar"]{background:#38516F!important}
/* Buttons */
.stButton>button,.stDownloadButton>button,.stLinkButton a{border-radius:10px!important;border:1px solid #3A5A78!important;background:linear-gradient(135deg,#19314B,#14243A)!important;color:#F1F7FF!important;font-weight:700!important;transition:all .18s ease}
.stButton>button:hover,.stDownloadButton>button:hover,.stLinkButton a:hover{border-color:#53E0D0!important;color:#72F1DF!important;box-shadow:0 0 0 3px #53E0D018}
/* Tables: native Streamlit dark theme is applied in show_table() */
[data-testid="stDataFrame"]{border:1px solid #314967!important;border-radius:12px!important;overflow:hidden!important;box-shadow:0 10px 26px #0003!important;background:#101A2B!important}
[data-testid="stDataFrame"] [role="columnheader"]{font-weight:700!important}
a {color:#65E9D8!important;text-decoration:none!important}
a:hover {color:#B9F36B!important;text-decoration:underline!important}
hr{border-color:#293E59!important}
div[data-testid="stAlert"]{background:#14263D;border:1px solid #365473;color:#EDF5FF;border-radius:12px}
section[data-testid="stSidebar"] .stRadio label{padding:6px 0}
[data-testid="stRadio"] label p{color:#DCE7F5!important;font-size:13px!important}
[data-testid="stRadio"] [role="radiogroup"] label[data-checked="true"] p{color:#65E9D8!important}
/* Cleaner dashboard hierarchy */
.block-container{max-width:1420px;padding-top:1.35rem!important}
.hero-shell{background:linear-gradient(115deg,#14263c 0%,#101c2e 58%,#122a35 100%);border:1px solid #2b4562;border-radius:22px;padding:27px 30px 24px;margin:2px 0 20px;box-shadow:0 18px 45px #0003}
.hero-kicker{font:600 10px 'DM Mono',monospace;letter-spacing:2px;color:#65e9d8;text-transform:uppercase;margin-bottom:10px}
.hero-title{font:700 clamp(32px,3.2vw,44px) 'Space Grotesk',sans-serif;color:#F7FAFF;letter-spacing:-1.6px;line-height:1.08;margin:0 0 9px}
.hero-sub{color:#C2D0E2;font-size:14px;line-height:1.55;margin:0;max-width:680px}
.filter-heading{font:700 11px 'DM Mono',monospace;letter-spacing:1.3px;color:#8fa9c5;text-transform:uppercase;margin:0 0 2px}
.table-wrap{width:100%;overflow:auto;border:1px solid #304763;border-radius:12px;background:#101a2b;margin:4px 0 12px}
.weather-table{border-collapse:collapse;width:100%;font-size:12px;color:#eaf2ff;line-height:1.4}
.weather-table thead th{position:sticky;top:0;background:#203650;color:#f2f7ff;font-weight:700;text-align:left;padding:10px 13px;border-bottom:1px solid #405977;white-space:nowrap}
.weather-table tbody td{background:#101a2b;color:#dce7f5;padding:9px 13px;border-bottom:1px solid #263b54;vertical-align:middle}
.weather-table tbody tr:nth-child(even) td{background:#15243a}
.weather-table tbody tr:last-child td{border-bottom:0}
[data-testid="stRadio"] [role="radiogroup"] label[data-checked="true"]>div:first-child{background:#53E0D0!important;border-color:#53E0D0!important}
/* A restrained, high-contrast refresh action (not a neon-green block) */
.stButton button[kind="primary"]{
  background:#173B4B!important;
  border:1px solid #3D8990!important;
  color:#E7FAFC!important;
  font-weight:700!important;
  min-height:44px!important;
  box-shadow:0 4px 14px #0002!important;
}
.stButton button[kind="primary"]:hover{
  background:#205463!important;
  border-color:#65D9D0!important;
  color:#FFFFFF!important;
}
.stButton button[kind="primary"]:focus{box-shadow:0 0 0 2px #65D9D044!important}
.stButton button[kind="primary"] p{color:inherit!important}
div[data-testid="stVerticalBlock"]{gap:.85rem}
div[data-testid="stHorizontalBlock"]{gap:1rem}

/* Compact empty-state status: avoid Streamlit success alert's oversized padding */
.status-inline{
  display:flex;align-items:center;gap:10px;flex-wrap:wrap;
  width:100%;box-sizing:border-box;padding:11px 14px;margin:5px 0 2px;
  min-height:0;border-radius:9px;background:#112A31;border:1px solid #28615F;
  color:#DDEFEF;font-size:12px;line-height:1.4;
}
.status-dot{width:7px;height:7px;flex:0 0 7px;border-radius:50%;background:#53E0D0;box-shadow:0 0 0 3px #53E0D01C}
.status-inline>span:nth-child(2){font-weight:700;color:#E8F8F7}
.status-detail{color:#9FBDBD;font-size:11px}
/* Responsive layout: tablet and mobile */
@media (max-width: 900px) {
  .block-container {padding:1.05rem 1.1rem 2rem!important;}\n  .hero-shell{padding:23px 22px 20px}\n   .filter-heading{margin-bottom:0}
  .hero-title {font-size:clamp(28px,6vw,40px)!important;line-height:1.12!important;letter-spacing:-1px!important;}
  .hero-sub {font-size:13px!important;}
  div[data-testid="stMetric"] {padding:13px!important;border-radius:13px!important;}
  div[data-testid="stMetric"] [data-testid="stMetricValue"] {font-size:clamp(21px,4vw,30px)!important;}
  [data-testid="stDataFrame"] {max-width:100%!important;}
}
@media (max-width: 640px) {
  .block-container {padding:.8rem .75rem 1.5rem!important;}\n  .hero-shell{padding:19px 17px 17px;border-radius:16px;margin-bottom:14px}\n  .hero-title{font-size:29px!important}\n   .filter-heading{font-size:10px}
  .hero-title {font-size:29px!important;line-height:1.12!important;}
  .hero-sub {font-size:12px!important;line-height:1.5!important;margin-bottom:12px!important;}
  h1 {font-size:1.55rem!important;} h2 {font-size:1.3rem!important;} h3 {font-size:1.15rem!important;}
  .panel-title {font-size:13px!important;}
  .panel-sub {font-size:10px!important;line-height:1.45!important;}
  div[data-testid="stMetric"] {padding:11px!important;min-height:92px;}
  div[data-testid="stMetric"] label {font-size:9px!important;}
  div[data-testid="stMetric"] [data-testid="stMetricValue"] {font-size:22px!important;}
  div[data-testid="stMetric"] [data-testid="stMetricValue"] div {white-space:normal!important;}
  .stButton>button,.stDownloadButton>button,.stLinkButton a {width:100%!important;min-height:42px!important;}
  [data-testid="stDataFrame"] {font-size:11px!important;}
  [data-testid="stSidebar"] {min-width: min(82vw, 300px)!important;}
  [data-testid="stPlotlyChart"] {width:100%!important;overflow:hidden!important;}
  [data-testid="stPlotlyChart"] iframe {max-width:100%!important;}
}
footer{visibility:hidden}
</style>
""", unsafe_allow_html=True)

# ---------- Data loading ----------
BUNDLED_CSV = ROOT / "reports" / "powerbi" / "weather-scope-india" / "data" / "WeatherScope_PowerBI_Import.csv"
PIPELINE_CSV = ROOT / "data" / "processed" / "weather_forecast.csv"
DB_PATH = ROOT / "data" / "processed" / "weather_pipeline.db"

WMO = {
    0:"Clear sky",1:"Mainly clear",2:"Partly cloudy",3:"Overcast",
    45:"Fog",48:"Depositing rime fog",
    51:"Light drizzle",53:"Moderate drizzle",55:"Dense drizzle",
    56:"Light freezing drizzle",57:"Dense freezing drizzle",
    61:"Slight rain",63:"Moderate rain",65:"Heavy rain",
    66:"Light freezing rain",67:"Heavy freezing rain",
    71:"Slight snowfall",73:"Moderate snowfall",75:"Heavy snowfall",
    77:"Snow grains",80:"Rain showers",81:"Moderate rain showers",
    82:"Violent rain showers",85:"Snow showers",86:"Heavy snow showers",
    95:"Thunderstorm",96:"Thunderstorm with hail",99:"Thunderstorm with heavy hail",
}

def find_data_file():
    # Prefer the actual pipeline output after a live refresh; otherwise use
    # the reproducible dashboard import dataset bundled with this repository.
    if PIPELINE_CSV.exists() and PIPELINE_CSV.stat().st_size > 0:
        return PIPELINE_CSV, "Pipeline output"
    return BUNDLED_CSV, "Bundled dashboard snapshot"

@st.cache_data(show_spinner=False)
def load_data(path_string: str, mtime: float) -> pd.DataFrame:
    df = pd.read_csv(path_string)
    df["forecast_date"] = pd.to_datetime(df["forecast_date"], errors="coerce")
    for col in ["temperature_2m_max","temperature_2m_min","precipitation_sum",
                "precipitation_probability_max","wind_speed_10m_max","temperature_range_c"]:
        if col in df:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    if "is_rain_risk" in df:
        df["is_rain_risk"] = df["is_rain_risk"].astype(str).str.lower().isin(["yes","true","1"])
    elif "precipitation_probability_max" in df:
        df["is_rain_risk"] = df["precipitation_probability_max"].ge(50)
    if "needs_review" in df:
        df["needs_review"] = df["needs_review"].astype(str).str.lower().isin(["yes","true","1"])
    else:
        df["needs_review"] = False
    if "weather_code" in df:
        df["weather_condition"] = pd.to_numeric(df["weather_code"],errors="coerce").map(WMO).fillna("Unknown")
    else:
        df["weather_condition"] = "Not available"
    return df.dropna(subset=["forecast_date"]).copy()

def style_chart(fig, height=330):
    fig.update_layout(
        height=height, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans",color="#E0EAF7",size=12),
        margin=dict(l=10,r=15,t=25,b=10),
        legend=dict(bgcolor="rgba(0,0,0,0)",orientation="h",y=1.12,x=0,font=dict(color="#DCE8F7",size=11)),
        xaxis=dict(showgrid=False,zeroline=False,linecolor="#405674",tickfont=dict(color="#C5D4E7")),
        yaxis=dict(gridcolor="#30445F",zeroline=False,tickfont=dict(color="#C5D4E7")),
        hoverlabel=dict(bgcolor="#15243a",bordercolor="#3c5876",font_color="#f1f6fc")
    )
    return fig

def panel_heading(title, subtitle=""):
    st.markdown(f'<div class="panel-title">{title}</div><div class="panel-sub">{subtitle}</div>',unsafe_allow_html=True)


def show_table(dataframe, height=None):
    """Render consistent, high-contrast tables across Streamlit versions."""
    table = dataframe.copy()
    numeric_cols = table.select_dtypes(include="number").columns
    for col in numeric_cols:
        if col in ["Rain Probability (%)"]:
            table[col] = table[col].map(lambda value: "—" if pd.isna(value) else f"{value:.0f}%")
        elif col in ["Rainfall (mm)", "Wind Speed (km/h)"]:
            table[col] = table[col].map(lambda value: "—" if pd.isna(value) else f"{value:.1f}")
        elif "Temp" in col or "Temperature" in col:
            table[col] = table[col].map(lambda value: "—" if pd.isna(value) else f"{value:.1f}")

    html_table = table.to_html(index=False, escape=True, border=0, classes="weather-table")
    max_height = f"max-height:{height}px;overflow:auto;" if height else ""
    st.markdown(
        f'<div class="table-wrap" style="{max_height}">{html_table}</div>',
        unsafe_allow_html=True,
    )

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown('<div style="font:800 18px Manrope;color:#eef5ff">◈ WeatherScope<span style="color:#58d6c5"> India</span></div>',unsafe_allow_html=True)
    st.caption("WEATHER INTELLIGENCE PLATFORM")
    st.markdown("---")
    page = st.radio("WORKSPACE",["Overview","City explorer","Rain & conditions","Data quality","About the pipeline"],label_visibility="visible")
    st.markdown("---")
    st.markdown('<span class="smallcaps">DATA SOURCE</span>',unsafe_allow_html=True)
    st.markdown("[Open-Meteo Forecast API ↗](https://open-meteo.com/en/docs)")
    st.caption("Forecast data provider · Five configured Indian cities")
    st.markdown("---")
    st.markdown("**Built by Shreya Y P**")
    st.link_button("GitHub repository ↗","https://github.com/shreyayp/weatherscope-india",use_container_width=True)
    st.caption("Portfolio project · 2026")

# ---------- Header / refresh ----------
data_path, source_label = find_data_file()
if not data_path.exists():
    st.error("No forecast dataset found. The bundled dashboard CSV should be included in the project ZIP.")
    st.stop()
mtime = data_path.stat().st_mtime
try:
    df_all = load_data(str(data_path),mtime)
except Exception as exc:
    st.error(f"Could not read forecast data: {exc}")
    st.stop()

# Hero: one clear title area, with refresh action placed beneath the description.
st.markdown(
    '<div class="hero-shell">'
    '<div class="hero-kicker">WEATHERSCOPE INDIA · WEATHER INTELLIGENCE</div>'
    '<div class="hero-title">Weather insights, made clear.</div>'
    '<p class="hero-sub">A focused view of temperature, rainfall and forecast quality across five Indian cities.</p>'
    '</div>',
    unsafe_allow_html=True,
)
action_col, source_col = st.columns([1.55, 3.45], vertical_alignment="center")
with action_col:
    if st.button("↻  Refresh forecast data", type="primary", use_container_width=True, help="Fetch a fresh forecast from Open-Meteo by running the project pipeline."):
        with st.spinner("Fetching forecast and running the pipeline…"):
            try:
                from src.pipeline import main
                main()
                load_data.clear()
                st.success("Forecast updated. Loading the latest data.")
                st.rerun()
            except Exception as exc:
                st.error(f"Refresh failed: {exc}. Your current snapshot is unchanged.")
with source_col:
    st.markdown(
        f'<div style="padding:4px 0 4px 10px"><span class="pill">● DATA SOURCE: {source_label.upper()}</span>'
        '<span style="font-size:12px;color:#AFC1D6;margin-left:12px">Refresh runs the ETL pipeline and reloads its output.</span></div>',
        unsafe_allow_html=True,
    )

# Filters shared by pages
cities = sorted(df_all["city"].dropna().unique().tolist())
st.markdown('<div class="filter-heading">FORECAST FILTERS</div>',unsafe_allow_html=True)
fc1,fc2,fc3 = st.columns([1.25,1.45,1.3], gap="large")
with fc1:
    selected_cities = st.multiselect("CITIES",cities,default=cities)
with fc2:
    min_date = df_all["forecast_date"].min().date()
    max_date = df_all["forecast_date"].max().date()
    date_range = st.date_input("FORECAST PERIOD",value=(min_date,max_date),min_value=min_date,max_value=max_date)
with fc3:
    threshold = st.slider("RAIN ALERT LEVEL",0,100,50,5,help="Highlight forecast days where rain probability meets or exceeds this level.")

if len(date_range)==2:
    start_date,end_date=date_range
else:
    start_date,end_date=min_date,max_date

filtered = df_all[
    df_all["city"].isin(selected_cities) &
    df_all["forecast_date"].dt.date.between(start_date,end_date)
].copy()
if filtered.empty:
    st.warning("No rows match these filters. Select a wider date range or more cities.")
    st.stop()
filtered["rain_risk_filtered"] = filtered["precipitation_probability_max"].ge(threshold)

# Snapshot timestamp, when present
fetched_label = "Snapshot date not supplied"
if "fetched_at_utc" in filtered.columns:
    try:
        fetched_label = str(filtered["fetched_at_utc"].dropna().iloc[0])
    except Exception:
        pass

# ---------- Pages ----------
if page == "Overview":
    st.markdown("### Executive overview")
    st.caption(f"Showing {len(filtered):,} forecast records · {filtered['city'].nunique()} cities · {start_date:%d %b} — {end_date:%d %b %Y}")
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("AVG MAX TEMPERATURE",f"{filtered['temperature_2m_max'].mean():.1f} °C")
    c2.metric("PEAK TEMPERATURE",f"{filtered['temperature_2m_max'].max():.1f} °C")
    c3.metric("AVG RAIN PROBABILITY",f"{filtered['precipitation_probability_max'].mean():.0f}%")
    c4.metric("RAIN-RISK DAYS",f"{int(filtered['rain_risk_filtered'].sum())}",help=f"Probability ≥ {threshold}%")
    st.markdown("")
    a,b=st.columns([1.45,1])
    with a:
        with st.container(border=True):
            panel_heading("Temperature outlook","Daily high and low temperatures · °C")
            palette={"Bengaluru":"#53E0D0","Mysuru":"#8BA7FF","Chennai":"#B9F36B","Hyderabad":"#C4A1FF","Mumbai":"#FF79B8"}
            fig=go.Figure()
            for city in sorted(filtered["city"].dropna().unique()):
                city_data=filtered[filtered["city"]==city].sort_values("forecast_date")
                color=palette.get(city,"#53E0D0")
                fig.add_trace(go.Scatter(x=city_data["forecast_date"],y=city_data["temperature_2m_max"],mode="lines+markers",name=city,
                    legendgroup=city,line=dict(color=color,width=2.8),marker=dict(size=6),
                    hovertemplate=f"{city}<br>%{{x|%d %b}}<br>High: %{{y:.1f}} °C<extra></extra>"))
                fig.add_trace(go.Scatter(x=city_data["forecast_date"],y=city_data["temperature_2m_min"],mode="lines+markers",name=f"{city} low",
                    legendgroup=city,showlegend=False,line=dict(color=color,width=1.8,dash="dot"),marker=dict(size=4),
                    hovertemplate=f"{city}<br>%{{x|%d %b}}<br>Low: %{{y:.1f}} °C<extra></extra>"))
            fig=style_chart(fig,340)
            fig.update_layout(legend=dict(orientation="h",y=1.12,x=0,font=dict(size=10)),hovermode="x unified")
            fig.update_yaxes(title="Temperature (°C)")
            fig.update_xaxes(title="")
            st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
            st.caption("Solid line = daily high · dotted line = daily low")
    with b:
        with st.container(border=True):
            panel_heading("City temperature ranking","Cities ranked by average daily high")
            city_temp=filtered.groupby("city",as_index=False)["temperature_2m_max"].mean().sort_values("temperature_2m_max")
            fig=px.bar(city_temp,x="temperature_2m_max",y="city",orientation="h",text_auto=".1f",
                       color="temperature_2m_max",color_continuous_scale=["#284c68","#53E0D0"])
            fig=style_chart(fig,340)
            fig.update_layout(coloraxis_showscale=False)
            fig.update_xaxes(title="Avg max temperature (°C)")
            fig.update_yaxes(title="")
            st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
    a,b=st.columns([1,1])
    with a:
        with st.container(border=True):
            panel_heading("Rain probability trend","Daily chance of precipitation by city · %")
            fig=px.line(filtered.sort_values("forecast_date"),x="forecast_date",y="precipitation_probability_max",color="city",
                        markers=True, line_shape="spline",
                        color_discrete_sequence=["#53E0D0","#8BA7FF","#B9F36B","#C4A1FF","#FF79B8"])
            fig=style_chart(fig,285)
            fig.update_traces(line=dict(width=2.8), marker=dict(size=6))
            fig.update_yaxes(title="Probability (%)",range=[0,100])
            fig.update_xaxes(title="")
            st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
    with b:
        with st.container(border=True):
            panel_heading("Rain alerts",f"Days with rain probability at or above {threshold}%")
            risk=filtered[filtered["rain_risk_filtered"]].sort_values("precipitation_probability_max",ascending=False)
            if risk.empty:
                st.success("No forecast records cross the selected rain-risk threshold.")
            else:
                view=risk[["city","forecast_date","precipitation_probability_max","precipitation_sum"]].copy()
                view["forecast_date"]=view["forecast_date"].dt.strftime("%d %b")
                view.columns=["City","Forecast Date","Rain Probability (%)","Rainfall (mm)"]
                view["Rainfall (mm)"] = view["Rainfall (mm)"].round(1)
                show_table(view,height=260)
    with st.container(border=True):
        panel_heading("Forecast records","Daily conditions and key weather measurements")
        cols=["city","forecast_date","weather_condition","temperature_2m_max","temperature_2m_min","precipitation_sum","precipitation_probability_max","wind_speed_10m_max"]
        detail=filtered[cols].sort_values(["city","forecast_date"]).copy()
        detail["forecast_date"]=detail["forecast_date"].dt.strftime("%d %b %Y")
        detail.columns=["City","Forecast Date","Weather Condition","Maximum Temp (°C)","Minimum Temp (°C)","Rainfall (mm)","Rain Probability (%)","Wind Speed (km/h)"]
        show_table(detail,height=320)
        st.download_button("↓ Download filtered forecast CSV",filtered.to_csv(index=False).encode("utf-8"),"weatherscope_filtered_forecast.csv","text/csv")

elif page == "City explorer":
    st.markdown("### City explorer")
    city_list=sorted(filtered["city"].unique())
    chosen=st.selectbox("SELECT A CITY",city_list)
    city_df=filtered[filtered["city"]==chosen].sort_values("forecast_date")
    current=city_df.iloc[0]
    m1,m2,m3,m4=st.columns(4)
    m1.metric("HIGHEST MAX TEMP",f"{city_df['temperature_2m_max'].max():.1f} °C")
    m2.metric("LOWEST MIN TEMP",f"{city_df['temperature_2m_min'].min():.1f} °C")
    m3.metric("TOTAL FORECAST RAIN",f"{city_df['precipitation_sum'].sum():.1f} mm")
    m4.metric("PEAK RAIN CHANCE",f"{city_df['precipitation_probability_max'].max():.0f}%")
    st.markdown("")
    l,r=st.columns([1.2,.8])
    with l:
        with st.container(border=True):
            panel_heading(f"{chosen} · temperature range","Daily max / min / range")
            fig=go.Figure()
            fig.add_trace(go.Scatter(x=city_df.forecast_date,y=city_df.temperature_2m_max,mode="lines+markers",name="Max",line=dict(color="#58d6c5",width=3)))
            fig.add_trace(go.Scatter(x=city_df.forecast_date,y=city_df.temperature_2m_min,mode="lines+markers",name="Min",line=dict(color="#83a0ff",width=3)))
            fig=style_chart(fig,350)
            fig.update_yaxes(title="°C")
            fig.update_xaxes(title="")
            st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
    with r:
        with st.container(border=True):
            panel_heading("Daily conditions","Expected weather conditions by day")
            for _,row in city_df.iterrows():
                st.markdown(f"""<div style="display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #26354b;padding:9px 1px">
                <div><div style="font-size:11px;color:#e5edf8">{row.forecast_date:%a, %d %b}</div><div style="font-size:10px;color:#8296af">{row.weather_condition}</div></div>
                <div style="text-align:right"><b style="font:600 16px Manrope;color:#58d6c5">{row.temperature_2m_max:.1f}°</b><div style="font-size:10px;color:#8da0b8">↓ {row.temperature_2m_min:.1f}°</div></div></div>""",unsafe_allow_html=True)
    with st.container(border=True):
        panel_heading("City forecast details","Rainfall, rain probability and wind speed")
        city_table = city_df[["forecast_date","weather_condition","precipitation_sum","precipitation_probability_max","wind_speed_10m_max"]].copy()
        city_table["forecast_date"] = city_table["forecast_date"].dt.strftime("%d %b %Y")
        show_table(city_table.rename(columns={
            "forecast_date":"Forecast Date","weather_condition":"Weather Condition","precipitation_sum":"Rainfall (mm)",
            "precipitation_probability_max":"Rain Probability (%)","wind_speed_10m_max":"Wind Speed (km/h)"
        }))

elif page == "Rain & conditions":
    st.markdown("### Rain & weather conditions")
    rain=filtered.copy()
    c1,c2,c3=st.columns(3)
    c1.metric("RAIN-RISK RECORDS",int(rain.rain_risk_filtered.sum()))
    c2.metric("FORECAST RAINFALL",f"{rain.precipitation_sum.sum():.1f} mm")
    c3.metric("MAX WIND SPEED",f"{rain.wind_speed_10m_max.max():.1f} km/h")
    l,r=st.columns(2)
    with l:
        with st.container(border=True):
            panel_heading("City rain probability","Average daily precipitation chance")
            avg=rain.groupby("city",as_index=False).precipitation_probability_max.mean().sort_values("precipitation_probability_max")
            fig=px.bar(avg,x="precipitation_probability_max",y="city",orientation="h",text_auto=".0f",
                       color="precipitation_probability_max",color_continuous_scale=["#284b66","#53E0D0"])
            fig=style_chart(fig,320);fig.update_layout(coloraxis_showscale=False);fig.update_xaxes(title="Probability (%)",range=[0,100]);fig.update_yaxes(title="")
            st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
    with r:
        with st.container(border=True):
            panel_heading("Rainfall outlook","Expected daily precipitation · mm")
            fig=px.bar(rain,x="forecast_date",y="precipitation_sum",color="city",barmode="group",
                       color_discrete_sequence=["#53E0D0","#8BA7FF","#B9F36B","#C4A1FF","#FF79B8"])
            fig=style_chart(fig,320);fig.update_yaxes(title="Rainfall (mm)");fig.update_xaxes(title="")
            st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
    with st.container(border=True):
        panel_heading("Rain alert events",f"Forecast records at or above the {threshold}% alert level")
        events=rain[rain.rain_risk_filtered].sort_values(["precipitation_probability_max"],ascending=False)
        if events.empty: st.success("No rain-risk records for the selected filters.")
        else:
            event_table = events[["city","forecast_date","precipitation_probability_max","precipitation_sum","wind_speed_10m_max","weather_condition"]].copy()
            event_table["forecast_date"] = event_table["forecast_date"].dt.strftime("%d %b %Y")
            show_table(event_table.rename(columns={
                "city":"City","forecast_date":"Forecast Date","precipitation_probability_max":"Rain Probability (%)",
                "precipitation_sum":"Rainfall (mm)","wind_speed_10m_max":"Wind Speed (km/h)","weather_condition":"Weather Condition"
            }))

elif page == "Data quality":
    st.markdown("### Data quality & pipeline health")
    total=len(filtered)
    needs=int(filtered.needs_review.sum())
    duplicate_count=int(filtered.duplicated(["city","forecast_date","fetched_at_utc"] if "fetched_at_utc" in filtered else ["city","forecast_date"]).sum())
    missing=int(filtered[["city","forecast_date","temperature_2m_max","temperature_2m_min","precipitation_sum","precipitation_probability_max"]].isna().any(axis=1).sum())
    a,b,c,d=st.columns(4)
    a.metric("ROWS IN VIEW",f"{total:,}")
    b.metric("FLAGGED FOR REVIEW",f"{needs:,}")
    c.metric("MISSING CRITICAL FIELDS",f"{missing:,}")
    d.metric("DUPLICATE SNAPSHOTS",f"{duplicate_count:,}")
    with st.container(border=True):
        panel_heading("Quality rule coverage","Rules implemented in src/transform.py")
        checks=[
            ("Forecast date is valid",int(filtered.forecast_date.isna().sum())),
            ("Maximum temperature present",int(filtered.temperature_2m_max.isna().sum())),
            ("Minimum temperature present",int(filtered.temperature_2m_min.isna().sum())),
            ("Precipitation probability within 0–100",int((~filtered.precipitation_probability_max.between(0,100)).sum())),
            ("Minimum temperature ≤ maximum",int((filtered.temperature_2m_min>filtered.temperature_2m_max).sum())),
            ("Wind speed is non-negative",int((filtered.wind_speed_10m_max<0).sum())),
        ]
        qdf=pd.DataFrame(checks,columns=["Validation rule","Rows failing rule"])
        qdf["Result"]=qdf["Rows failing rule"].map(lambda x:"PASS" if x==0 else "REVIEW")
        show_table(qdf)
    with st.container(border=True):
        panel_heading("Rows requiring review","Quality flags from the transformation pipeline")
        if "quality_flags" in filtered.columns:
            flagged=filtered[filtered.needs_review | filtered.quality_flags.fillna("").ne("")]
            if flagged.empty:
                st.markdown(
                    '<div class="status-inline"><span class="status-dot"></span>'
                    '<span>No records currently flagged</span>'
                    '<span class="status-detail">All checked rows passed the available review checks.</span></div>',
                    unsafe_allow_html=True,
                )
            else: show_table(flagged)
        else:
            st.info("The bundled Power BI import file does not include detailed quality flag text. Run the pipeline to generate the full quality metadata.")
    st.caption("The bundled dashboard CSV is a reproducible snapshot. Pipeline quality metadata is more complete when generated by running the live ETL workflow.")

else:
    st.markdown("### About the WeatherScope pipeline")
    st.write("WeatherScope India is an API-driven weather analytics project that collects short-range forecasts for five configured Indian cities, transforms and validates the records, stores timestamped snapshots in SQLite and exports reports for analysis.")
    st.markdown("#### Data flow")
    st.code("Open-Meteo Forecast API\n        ↓\nExtraction (src/extract.py)\n        ↓\nTransformation & validation (src/transform.py)\n        ↓\nSQLite snapshot storage (src/load.py)\n        ↓\nSQL analysis + CSV / JSON reports\n        ↓\nStreamlit analytics experience")
    st.markdown("#### Configured cities")
    show_table(pd.DataFrame([
        {"City":"Bengaluru","State":"Karnataka"},
        {"City":"Mysuru","State":"Karnataka"},
        {"City":"Chennai","State":"Tamil Nadu"},
        {"City":"Hyderabad","State":"Telangana"},
        {"City":"Mumbai","State":"Maharashtra"},
    ]))
    st.markdown("#### Data source & project links")
    st.markdown("Weather forecasts are provided by [Open-Meteo Forecast API ↗](https://open-meteo.com/en/docs).")
    st.link_button("WeatherScope India on GitHub ↗","https://github.com/shreyayp/weatherscope-india")
    st.caption("Forecasts are model-based estimates, not observations or guarantees. The included CSV is a dated snapshot; use Refresh live data to run the pipeline and fetch a new forecast.")
st.markdown("---")
st.caption(f"WEATHERSCOPE INDIA · DATA SNAPSHOT: {fetched_label} · PYTHON / PANDAS / SQLITE / STREAMLIT")
