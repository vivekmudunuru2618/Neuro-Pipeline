import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="EEG + Ad Metrics Dashboard", layout="wide")

# ---------- Paths ----------
DATA_PATH = "../include/data/analysis"
PLOT_PATH = "../include/plots"

# ---------- Load Data ----------
@st.cache_data
def load_data():
    df = pd.read_csv(os.path.join(DATA_PATH, "cleaned_eeg.csv"))
    df.columns = df.columns.str.strip().str.lower()
    return df

df = load_data()

st.title("🧠 EEG + Marketing Metrics Dashboard")
st.markdown("Visualize per-stimulus insights from EEG and marketing data")

# ---------- Stimulus Selector ----------
st.sidebar.header("🔍 Filter")
stimuli = df["sourcestimuliname"].dropna().unique()
selected = st.sidebar.multiselect("Select Stimuli", sorted(stimuli), default=list(stimuli))

filtered_df = df[df["sourcestimuliname"].isin(selected)]

# ---------- KPI Overview ----------
st.subheader("📊 Summary Statistics")
numeric_cols = ['engagement', 'emotion', 'cognitiveload', 'desire', 'memorisation', 'impact',
                'synchrony', 'purchase_intent', 'brand_stickiness', 'unaided_recall', 'preference']

summary = filtered_df[numeric_cols].mean().round(2).to_frame("Average Value")
st.dataframe(summary)

# ---------- Bar Chart by Stimulus ----------
st.subheader("📈 Attribute per Stimulus")

attribute = st.selectbox("Select attribute to visualize", numeric_cols)
grouped = filtered_df.groupby("sourcestimuliname")[attribute].mean().sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(12, 5))
grouped.plot(kind="bar", ax=ax, color='skyblue')
ax.set_ylabel(attribute.title())
ax.set_title(f"{attribute.title()} per Stimulus")
plt.xticks(rotation=45)
st.pyplot(fig)

# ---------- Benchmark Composite Score ----------
st.subheader("🏁 Benchmarking: Attention + Engagement + Memorisation")
if all(x in filtered_df.columns for x in ['engagement', 'memorisation', 'emotion']):
    benchmark_df = (
        filtered_df.groupby("sourcestimuliname")[['engagement', 'memorisation', 'emotion']]
        .mean()
    )
    benchmark_df["composite_score"] = benchmark_df.sum(axis=1)
    st.dataframe(benchmark_df.sort_values("composite_score", ascending=False).round(2))
else:
    st.warning("⚠️ Not all benchmark columns found in dataset.")

# ---------- Image Gallery (Optional) ----------
st.subheader("🖼️ Generated Plots (from Airflow DAG)")
plot_images = [f for f in os.listdir(PLOT_PATH) if f.endswith(".png")]
for img_file in plot_images:
    st.image(os.path.join(PLOT_PATH, img_file), caption=img_file)

metrics = ["engagement", "emotion", "cognitiveload", "desire", "memorisation", "impact", "synchrony"]

import numpy as np

@st.cache_data
def simulate_time_series(df, metric, stimulus):
    # Filter for the selected stimulus
    row = df[df["sourcestimuliname"] == stimulus].copy()
    
    # Check if we have data
    if row.empty:
        return pd.DataFrame()
    
    # Generate 10 synthetic time points
    n_points = 10
    base_val = row[metric].values[0]
    np.random.seed(42)
    variation = np.random.normal(loc=0, scale=1.5, size=n_points)
    
    time_series_df = pd.DataFrame({
        "time_point": range(n_points),
        metric: base_val + variation
    })
    return time_series_df


st.markdown("### ⏱️ Time-Series Pattern for EEG Metrics")

selected_metric = st.selectbox("Choose a metric to visualize over time", options=metrics)
selected_stimulus = st.selectbox("Choose stimulus for time-series", options=df["sourcestimuliname"].unique())

ts_df = simulate_time_series(df, selected_metric, selected_stimulus)

if not ts_df.empty:
    fig_ts, ax_ts = plt.subplots()
    ax_ts.plot(ts_df["time_point"], ts_df[selected_metric], marker="o")
    ax_ts.set_title(f"{selected_metric.title()} Over Time for {selected_stimulus}")
    ax_ts.set_xlabel("Simulated Time Point")
    ax_ts.set_ylabel(selected_metric.title())
    st.pyplot(fig_ts)
else:
    st.warning("No data available for the selected stimulus.")



st.success("✅ Dashboard loaded successfully.")
