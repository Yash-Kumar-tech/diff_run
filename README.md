# diff_run

A lightweight, local-first ML experiment tracking system and configuration diff tool. 

diff_run provides a developer-centric alternative to heavy cloud-based platforms. It combines a simple Python SDK for logging metrics and media, a SQLite-backed FastAPI server, and a standalone React frontend to analyze your machine learning experiments running purely on your local machine.

## Core Features

- **Zero-setup Tracking**: Log metrics, model configurations, and system resources directly to a local SQLite database without cloud dependencies.
- **Media Artifact Logging**: Support for logging visual (images) and auditory (audio waveforms) outputs from models to local storage.
- **Smart Configuration Diffing**: Analyzes hyperparameter configs across runs, highlighting additions, removals, and significant numeric shifts.
- **Environment Capture**: Auto-logs git commit hashes and repository dirty states.
- **Local Dashboard**: A React and Vite-powered frontend for reviewing and analyzing your runs.

## Tech Stack

- **Backend**: Python, FastAPI, SQLite
- **Frontend**: React, Vite, Recharts, Lucide Icons
- **SDK**: Vanilla Python with optional integration for `psutil`, `Pillow`, and `scipy`.

## Getting Started

### 1. Installation

Clone the repository:

```bash
git clone https://github.com/Yash-Kumar-tech/diff_run.git
cd diff_run
```

Ensure you have the required Python libraries for the backend and optional SDK tracking features:

```bash
pip install fastapi uvicorn pillow scipy psutil numpy
```

Install the frontend dependencies:

```bash
cd frontend
npm install
```

### 2. Running the Platform

You need to run both the FastAPI backend and the Vite development server.

**Start the Backend API:**
```bash
# Run from the project root directory
uvicorn backend.main:app --reload
```
The API and media artifacts will be served at `http://localhost:8000`.

**Start the Frontend Dashboard:**
```bash
# Run from the frontend directory
cd frontend
npm run dev
```
The UI dashboard will be accessible at `http://localhost:5173`.

### 3. Usage Example

Integrate the tracker into your existing ML codebase in just a few lines:

```python
from tracker.experiment import Experiment
import numpy as np

# Instantiate the logger
exp = Experiment("my_classifier_project")

# Log configurations
exp.log_config({
    "learning_rate": 0.001,
    "batch_size": 32,
    "optimizer": "Adam"
})

# Log metrics during training loop
for step in range(100):
    loss = 1.0 / (step + 1)
    
    # Log primitive scalars
    exp.log_metric("loss", loss, step=step)
    
    # Log system CPU and Memory percentages
    exp.log_system_metrics(step=step)

# Log media outputs at specific intervals (requires Pillow)
dummy_image = np.zeros((100, 100, 3), dtype=np.uint8)
exp.log_image("sample_output", dummy_image, step=100)
```

## Roadmap

- [x] Python Logging SDK
- [x] Run List & Detail Dashboard
- [x] Config Diff Engine Logic
- [x] Image & Audio Support
- [ ] Multi-run visual comparison overlays
- [ ] Integration of the Diff Engine insights into the React Dashboard
- [ ] Advanced artifact exploration (dataframes, point clouds)

## License

MIT
