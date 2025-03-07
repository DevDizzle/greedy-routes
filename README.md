# Greedy Routes"

This repository contains the **Greedy Routes** for multi-scenario route optimization using Google’s Route Optimization API and a multi-LLM approach.

## Project Structure

    greedy-routes/
    ├── app/
    │   ├── __init__.py                 # Makes `app` a Python package
    │   ├── main.py                     # FastAPI entrypoint
    │   ├── orchestrator.py             # Orchestrates LLM calls & scenario logic
    │   ├── router_llm.py              # Router LLM for scenario classification
    │   ├── scenario_specialist_fleet.py
    │   ├── scenario_specialist_tsp.py
    │   ├── scenario_specialist_pickup_delivery.py
    │   └── ...                         # Additional scenario files
    ├── google_route_api.py             # Wrapper to call Google Route Optimization API
    ├── post_processor.py               # CSV/PDF or other output formatting
    ├── tests/
    │   └── test_router_llm.py          # Example pytest file
    ├── requirements.txt                # Python dependencies
    ├── Dockerfile                      # Docker build instructions
    ├── cloudbuild.yaml                 # CI/CD pipeline for Cloud Build → Cloud Run
    └── README.md                       # This file

## Quick Start

1. **Clone or Pull** the repo:
    ```bash
    git clone https://github.com/<YourUsername>/<YourRepoName>.git
    ```
2. **Install Dependencies** locally or in Cloud Shell:
    ```bash
    pip install -r requirements.txt
    ```
3. **Run FastAPI Locally**:
    ```bash
    uvicorn app.main:app --host 0.0.0.0 --port 8080
    ```
    Then open your browser at [http://127.0.0.1:8080](http://127.0.0.1:8080).

4. **Test** with Pytest:
    ```bash
    pytest
    ```
    This runs any tests under `tests/`.

## Deployment (Cloud Run)

- **Build & Push** via Cloud Build (manual one-off):
    ```bash
    gcloud builds submit --config=cloudbuild.yaml .
    ```
- Or set up a **trigger** in Cloud Build to deploy automatically when pushing to `main`.

## Environment Variables

- `GEMINI_API_KEY`: PaLM/Gemini key for the Router LLM calls.  
- `PROJECT_ID`: Google Cloud project ID (if you need it in scripts).  

For secure secrets, use **Google Secret Manager** and **--set-secrets** when deploying to Cloud Run.

## TODO

- Implement real calls in `google_route_api.py` to the Google Cloud Fleet Routing API.
- Add parameter extraction logic in each specialist (Fleet, TSP, Pickup-Delivery, etc.).
- Build a simple React front-end to chat with the `/api/optimize` endpoint.
- Handle multi-turn user interactions (time window requests, capacity constraints, etc.).

---

Happy coding, and welcome to **Greedy Routes**!
