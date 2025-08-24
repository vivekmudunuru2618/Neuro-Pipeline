# 🧠 Neuro-Pipeline: EEG & Ad Metrics Analysis with Airflow + Streamlit

An end-to-end, production-style data pipeline built to process neuroscience-derived EEG metrics alongside ad metadata, orchestrated with **Apache Airflow** (via **Astronomer**) and visualized through an interactive **Streamlit dashboard**.

This project was built as a hands-on, modular, and scalable solution to demonstrate advanced data engineering and analysis skills—especially in response to a real-world hiring challenge from Future Proof Insights.

---

## 🚀 Project Highlights

- ⛓️ **ETL Pipeline with Apache Airflow**
- 🧠 **EEG stimulus-level & ad category-level analysis**
- 📊 **Marketing metric benchmarking & reporting**
- 📈 **Interactive Streamlit dashboard with time-series simulation**
- ☁️ **Designed for cloud-readiness, API inputs, and modular growth**

---

## 📦 Tech Stack

| Tool             | Purpose                                      |
|------------------|----------------------------------------------|
| **Python**       | Core data transformation and logic           |
| **Apache Airflow** | Orchestration of ETL tasks via DAGs        |
| **Astronomer CLI**| Seamless local Airflow development          |
| **Pandas**       | Data wrangling and statistical operations    |
| **Matplotlib**   | Visualizations and reporting plots           |
| **Streamlit**    | Frontend dashboard for interactive insights  |
| **Docker**       | (Optional) Containerization and reproducibility |

---

## 🗂️ Project Structure

airflow-neuro-pipeline/
├── dags/ # Airflow DAG logic
│ └── neuro_analysis_dag.py
├── include/
│ ├── data/
│ │ └── analysis/
│ │ ├── File2.csv # EEG input data
│ │ ├── File3.xlsx # Ad metadata
│ │ ├── cleaned_eeg.csv # Cleaned EEG + marketing data
│ │ ├── stimulus_summary.csv # Per-stimulus metrics
│ │ ├── benchmark_summary.csv # Composite score benchmark
│ │ └── category_summary.csv # Per-category analysis
│ └── plots/ # Auto-generated plots
├── streamlit_app/
│ └── app.py # Streamlit dashboard code
├── requirements.txt # Python dependencies
├── Dockerfile # Container setup
├── README.md # Project documentation
└── airflow_settings.yaml # Airflow connection config

yaml
Copy
Edit

---

## ⚙️ Setup Instructions

### 📍 Prerequisites

- [Astronomer CLI](https://docs.astronomer.io/astro/install-cli) (for Airflow)
- Python 3.8+
- Docker (optional)

### 🔁 Run the Airflow DAG

```bash
# Start Airflow with Astronomer
astro dev start
Navigate to http://localhost:8080 to access the Airflow UI. Run the DAG neuro_analysis_dag.

📊 Launch the Streamlit Dashboard
In a new terminal:

bash
Copy
Edit
cd streamlit_app
streamlit run app.py
Dashboard will be available at: http://localhost:8501

📈 Features in Detail
✅ Airflow DAG Tasks
preprocess_eeg_data: Clean EEG & metric dataset

stimulus_level_analysis: Group by ad stimulus

benchmark_ads: Generate composite metric scores

generate_eeg_plots: Output visuals for key metrics

preprocess_ad_metadata: Clean and prep ad metadata

category_level_analysis: Group metrics by ad category

generate_metadata_plots: Bar charts for preference, brand stickiness, etc.

streamlit_ready_trigger: Final sync stage

📊 Streamlit Dashboard
Filter by stimulus

View summary KPIs across metrics

Visualize per-stimulus performance

Benchmark composite rankings

Gallery of all Airflow-generated plots

Simulated time-series EEG patterns (bonus visualization)

📌 Motivation & Background
This project was created as a self-driven follow-up to a real hiring challenge I received from Future Proof Insights in March 2025. Though not selected at the time, I transformed the opportunity into a learning experience—building a fully functional system that exceeds the original task brief with automation, modularity, and end-to-end transparency.

🤝 Contact
Venkata Vivek Kumar Mudunuru
Data Engineer | Python Developer | EEG x Marketing Analyst
📍 Dublin, Ireland
📫 LinkedIn | ✉️ vivekmudunuru2618@gmail.com

🌟 Future Plans
Integrate with cloud-based EEG datasets

Stream real-time inputs via API or Kafka

Deploy Streamlit on HuggingFace or Streamlit Cloud

Add advanced time-series analysis (RNN, FFT, etc.)

🧠 Inspired by
Neuroscience + Adtech data fusion

Future Proof Insights application process

Personal growth through rejection & adaptation
