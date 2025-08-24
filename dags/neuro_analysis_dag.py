from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os
import pandas as pd
import matplotlib.pyplot as plt

# -------------------- Paths --------------------
BASE_DIR = "/usr/local/airflow/include"
ANALYSIS_DIR = os.path.join(BASE_DIR, "data", "analysis")
EEG_RAW = os.path.join(ANALYSIS_DIR, "File2.csv")
EEG_CLEAN = os.path.join(ANALYSIS_DIR, "cleaned_eeg.csv")
EEG_SUMMARY = os.path.join(ANALYSIS_DIR, "stimulus_summary.csv")
BENCHMARK = os.path.join(ANALYSIS_DIR, "benchmark_summary.csv")

META_RAW = os.path.join(ANALYSIS_DIR, "File3.xlsx")
META_CLEAN = os.path.join(ANALYSIS_DIR, "cleaned_metadata.csv")
CATEGORY_SUMMARY = os.path.join(ANALYSIS_DIR, "category_summary.csv")

PLOT_DIR = os.path.join(BASE_DIR, "plots")
REPORT_DIR = os.path.join(BASE_DIR, "reports")

# -------------------- EEG Preprocessing --------------------
def preprocess_eeg():
    df = pd.read_csv(EEG_RAW)
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    df.dropna(subset=["sourcestimuliname"], inplace=True)
    df.to_csv(EEG_CLEAN, index=False)
    print(f"✅ EEG Preprocessed: {df.shape[0]} rows")

# -------------------- EEG Stimulus Analysis --------------------
def stimulus_level_analysis():
    df = pd.read_csv(EEG_CLEAN)
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    result = df.groupby("sourcestimuliname")[numeric_cols].mean().reset_index()
    result.to_csv(EEG_SUMMARY, index=False)
    print("📊 Stimulus-level summary saved.")

# -------------------- EEG Benchmark --------------------
def benchmark_ads():
    df = pd.read_csv(EEG_CLEAN)
    if {"attention", "engagement", "memorisation", "sourcestimuliname"}.issubset(df.columns):
        benchmark = df.groupby("sourcestimuliname")[["attention", "engagement", "memorisation"]].mean()
        benchmark["composite"] = benchmark.sum(axis=1)
        benchmark = benchmark.sort_values("composite", ascending=False).reset_index()
        benchmark.to_csv(BENCHMARK, index=False)
        print("🏁 Benchmark summary created.")

# -------------------- EEG Plots --------------------
def generate_eeg_plots():
    df = pd.read_csv(EEG_SUMMARY)
    os.makedirs(PLOT_DIR, exist_ok=True)
    for col in ["attention", "engagement", "emotion", "memorisation"]:
        if col in df.columns:
            plt.figure(figsize=(10, 6))
            plt.bar(df["sourcestimuliname"], df[col], color='skyblue')
            plt.title(f"{col.title()} per Stimulus")
            plt.xticks(rotation=90)
            plt.tight_layout()
            path = os.path.join(PLOT_DIR, f"{col}_per_stimulus.png")
            plt.savefig(path)
            plt.close()
            print(f"📈 Saved: {path}")

# -------------------- Metadata Preprocessing --------------------
def preprocess_metadata():
    df = pd.read_excel(META_RAW)
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    df.to_csv(META_CLEAN, index=False)
    print("✅ Metadata cleaned.")

# -------------------- Category-Level Analysis --------------------
def category_level_analysis():
    df = pd.read_csv(META_CLEAN)
    if "category" in df.columns:
        num_cols = df.select_dtypes(include='number').columns.tolist()
        summary = df.groupby("category")[num_cols].mean().reset_index()
        summary.to_csv(CATEGORY_SUMMARY, index=False)
        print("📊 Category-level analysis saved.")
    else:
        print("⚠️ 'category' column not found.")

# -------------------- Metadata Plots --------------------
def generate_metadata_plots():
    df = pd.read_csv(CATEGORY_SUMMARY)
    for metric in ["purchase_intent", "preference", "brand_stickiness"]:
        if metric in df.columns:
            plt.figure(figsize=(8, 5))
            plt.bar(df["category"], df[metric], color='green')
            plt.title(f"{metric.title()} by Category")
            plt.xticks(rotation=45)
            plt.tight_layout()
            path = os.path.join(PLOT_DIR, f"{metric}_by_category.png")
            plt.savefig(path)
            plt.close()
            print(f"📉 Saved: {path}")

# -------------------- Final Placeholder --------------------
def notify_ready():
    print("✅ All outputs generated. Ready for Streamlit.")

# -------------------- DAG Definition --------------------
default_args = {
    'start_date': datetime(2025, 8, 21),
}

with DAG(
    dag_id="neuro_analysis_dag",
    start_date=datetime(2025, 8, 21),
    schedule="@once",
    catchup=False,
    tags=["neuro", "eeg", "modular"]
) as dag:

    t1 = PythonOperator(task_id="preprocess_eeg_data", python_callable=preprocess_eeg)
    t2 = PythonOperator(task_id="stimulus_level_analysis", python_callable=stimulus_level_analysis)
    t3 = PythonOperator(task_id="benchmark_ads", python_callable=benchmark_ads)
    t4 = PythonOperator(task_id="generate_eeg_plots", python_callable=generate_eeg_plots)

    t5 = PythonOperator(task_id="preprocess_ad_metadata", python_callable=preprocess_metadata)
    t6 = PythonOperator(task_id="category_level_analysis", python_callable=category_level_analysis)
    t7 = PythonOperator(task_id="generate_metadata_plots", python_callable=generate_metadata_plots)

    t8 = PythonOperator(task_id="streamlit_ready_trigger", python_callable=notify_ready)

    t1 >> [t2, t3] >> t4
    t5 >> [t6, t7]
    [t4, t7] >> t8
