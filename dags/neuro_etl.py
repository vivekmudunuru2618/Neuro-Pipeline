from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import os
from pathlib import Path

# Folders
EEG_DIR = '/usr/local/airflow/include/data/eeg_raw'
EYE_DIR = '/usr/local/airflow/include/data/eye_raw'
PROCESSED_DIR = '/usr/local/airflow/include/data/processed'
os.makedirs(PROCESSED_DIR, exist_ok=True)

# Function to clean and standardize Timestamp column
def clean_and_prepare(df, source):
    df.columns = df.columns.str.strip()
    if "Timestamp" in df.columns:
        df["Timestamp"] = pd.to_numeric(df["Timestamp"], errors='coerce') * 1000
        df = df[pd.to_numeric(df["Timestamp"], errors='coerce').notnull()]
        df["Timestamp"] = df["Timestamp"].astype(float)
    if "SourceStimuliName" in df.columns:
        df["SourceStimuliName"] = df["SourceStimuliName"].astype(str).str.strip().str.lower()
    df['source_file'] = source
    return df

# 1. Extract
def extract_data():
    def find_data_start(file_path):
        with open(file_path, 'r', encoding="utf-8") as f:
            for i, line in enumerate(f):
                if "#DATA" in line:
                    return i + 1
        return None

    def read_and_process(folder):
        dfs = []
        for file in os.listdir(folder):
            if file.endswith('.csv'):
                path = os.path.join(folder, file)
                start_row = find_data_start(path)
                if start_row is None:
                    continue
                df = pd.read_csv(path, skiprows=start_row, low_memory=False)
                df['FileName'] = file
                dfs.append(df)
        return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()

    eeg_df = read_and_process(EEG_DIR)
    eye_df = read_and_process(EYE_DIR)

    eeg_df.to_csv(f"{PROCESSED_DIR}/eeg_all.csv", index=False)
    eye_df.to_csv(f"{PROCESSED_DIR}/eye_all.csv", index=False)

# 2. Transform
def transform_data():
    import pandas as pd

    eeg_path = f"{PROCESSED_DIR}/eeg_all.csv"
    eye_path = f"{PROCESSED_DIR}/eye_all.csv"

    eeg_df = pd.read_csv(eeg_path, low_memory=False)
    eye_df = pd.read_csv(eye_path, low_memory=False)

    # --- Ensure timestamp column is clean ---
    for df in [eeg_df, eye_df]:
        if 'Timestamp' not in df.columns:
            raise ValueError("Missing 'Timestamp' column in input data.")

    eeg_df['Timestamp'] = pd.to_numeric(eeg_df['Timestamp'], errors='coerce')
    eye_df['Timestamp'] = pd.to_numeric(eye_df['Timestamp'], errors='coerce')

    eeg_df = eeg_df.dropna(subset=['Timestamp']).sort_values(by='Timestamp')
    eye_df = eye_df.dropna(subset=['Timestamp']).sort_values(by='Timestamp')

    # --- Run merge_asof ---
    merged = pd.merge_asof(
        eeg_df,
        eye_df,
        on='Timestamp',
        direction='nearest',
        suffixes=('_eeg', '_eye')
    )

    merged.to_csv(f"{PROCESSED_DIR}/merged_clean.csv", index=False)

# 3. Load
def load_data():
    df = pd.read_csv(f"{PROCESSED_DIR}/merged_clean.csv")
    df.to_parquet(f"{PROCESSED_DIR}/final_output.parquet", index=False)

# DAG definition
with DAG(
    dag_id='neuro_etl_pipeline',
    start_date=datetime(2023, 1, 1),
    schedule=None,
    catchup=False,
    description='ETL Pipeline for EEG + Eye tracking fusion'
) as dag:

    t1 = PythonOperator(task_id='extract', python_callable=extract_data)
    t2 = PythonOperator(task_id='transform', python_callable=transform_data)
    t3 = PythonOperator(task_id='load', python_callable=load_data)

    t1 >> t2 >> t3