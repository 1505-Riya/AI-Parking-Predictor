# AI-Powered Smart Parking Availability Predictor

**Codeversity - Round 2 Submission**

## 📌 Project Overview

Urban congestion in Surat is significantly impacted by inefficient parking searches. This project provides a **Near Real-Time Geospatial Dashboard** that integrates official **Surat Municipal Corporation (SMC)** datasets with a **Temporal Heuristic Predictive Model**.

The system allows citizens to visualize parking availability across 80+ sites, forecast occupancy based on time-of-day trends, and interact with an AI Decision Support system for routing.

## 🧠 How It Works: The "Data-to-AI" Pipeline

The application operates through a three-tier architecture:

### 1. Robust Data Ingestion Layer

The backend ingests the official `D58-Parking Lots.csv` dataset. Unlike static viewers, our engine features:

- **Encoding Resilience**: Automatically handles multi-format CSV encodings (`UTF-8`, `Latin1`) to prevent data crashes during ingestion.
- **Coordinate Normalization**: A custom processing layer that sanitizes non-standard geospatial strings and handles potential null values to ensure 100% map rendering reliability.
- **Integrity Checks**: Safely handles "NaN" or empty capacity cells by defaulting to zero-values rather than failing the process.

### 2. Predictive Analytics Engine

Instead of relying on flat, static data, we apply a **Temporal Intelligence Engine**:

- **Temporal Weighting**: The model recognizes urban "Peak Hour" profiles (Office/Commercial surges between 10 AM – 1 PM and Leisure/Market surges between 6 PM – 9 PM).
- **Stochastic Variance (Near Real-Time Simulation)**: To mimic live IoT sensor behavior, the system applies Gaussian jitter to static capacity records, providing a dynamic "stream" that updates every 5 seconds.
- **Confidence Scoring**: An AI confidence metric is generated based on data proximity to known peak variance hours.

### 3. Geospatial Visualization (Leaflet.js)

The frontend utilizes a high-performance GIS layer:

- **Dynamic Clustering**: Renders 80+ parking hubs with zero performance lag.
- **Heat-Mapped Status**: Color-coded markers (Green > 70%, Amber > 30%, Red < 30%) allow for sub-2-second decision-making by users.

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python) - Selected for asynchronous high-speed API handling.
- **Frontend**: Leaflet.js (Mapping), Tailwind CSS (UI), JavaScript (ES6+).
- **Data Science**: Pandas, NumPy (Data Sanitization & Modeling).
- **Server**: Uvicorn.

## 🚦 Installation & Deployment

1.  **Ensure** `D58-Parking Lots.csv` is in the root directory.
2.  **Install Dependencies**:
    ```bash
    pip install fastapi uvicorn pandas numpy pydantic
    ```
3.  **Launch Server**:
    ```bash
    python main.py
    ```
4.  **Open Dashboard**: Navigate to `http://127.0.0.1:8000`

## 🚀 Future Scope & Scalability

### Phase 1: National Data Exchange (IUDX)

Transitioning from simulated jitter to live magnetic/ultrasonic sensor feeds from Surat's ICCC (Integrated Command and Control Centre) via the **India Urban Data Exchange**.

### Phase 2: ML Model Advancement

Transitioning from heuristic logic to a **Random Forest Regressor** or **LSTM (Long Short-Term Memory)** neural network trained on historical SMC occupancy data to account for seasonal variations.

### Phase 3: Regional Portability

The architecture is strictly city-agnostic. By swapping the CSV data source and adjusting the geospatial center, the solution can be scaled to any Smart City in India in minutes.
