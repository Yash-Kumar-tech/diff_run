import os
import sqlite3
import pytest
import numpy as np

from tracker import Experiment

def test_experiment_creation(tmp_path):
    db_path = str(tmp_path / "tracker.db")
    artifacts_dir = str(tmp_path / "artifacts")
    
    exp = Experiment("test_project", db_path=db_path, artifacts_dir=artifacts_dir)
    
    assert os.path.exists(db_path)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT project, status FROM runs WHERE id=?", (exp.run_id,))
    row = cursor.fetchone()
    assert row is not None
    assert row[0] == "test_project"
    assert row[1] == "running"
    conn.close()

def test_log_metric(tmp_path):
    db_path = str(tmp_path / "tracker.db")
    exp = Experiment("test_project", db_path=db_path, artifacts_dir=str(tmp_path / "art"))
    
    exp.log_metric("loss", 0.5, step=1)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name, value, step FROM metrics WHERE run_id=?", (exp.run_id,))
    row = cursor.fetchone()
    assert row is not None
    assert row[0] == "loss"
    assert row[1] == 0.5
    assert row[2] == 1
    conn.close()
    
def test_log_config(tmp_path):
    db_path = str(tmp_path / "tracker.db")
    exp = Experiment("test_project", db_path=db_path, artifacts_dir=str(tmp_path / "art"))
    
    config = {"lr": 0.01, "batch_size": 32}
    exp.log_config(config)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT config_json FROM configs WHERE run_id=?", (exp.run_id,))
    row = cursor.fetchone()
    assert row is not None
    assert '"lr":' in row[0] or '"lr": 0.01' in row[0]
    conn.close()
