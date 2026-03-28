from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
import sqlite3
import json
import os

from tracker.diff_engine import DiffEngine

router = APIRouter()

DB_PATH = os.environ.get("DIFF_RUN_DB", "./.diff_run/tracker.db")

def _get_conn():
    if not os.path.exists(DB_PATH):
        # Prevent errors before any runs are logged
        open(DB_PATH, 'a').close()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@router.get("/")
def list_runs():
    try:
        with _get_conn() as conn:
            cur = conn.cursor()
            # Fails gracefully if table doesn't exist yet
            cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='runs'")
            if not cur.fetchone():
                return []
                
            cur.execute("SELECT * FROM runs ORDER BY start_time DESC")
            return [dict(row) for row in cur.fetchall()]
    except Exception as e:
        return []

@router.get("/{run_id}")
def get_run(run_id: str):
    try:
        with _get_conn() as conn:
            cur = conn.cursor()
            
            # Run Metadata
            cur.execute("SELECT * FROM runs WHERE id=?", (run_id,))
            run_row = cur.fetchone()
            if not run_row:
                raise HTTPException(404, "Run not found")
                
            # Metrics
            cur.execute("SELECT * FROM metrics WHERE run_id=? ORDER BY step ASC", (run_id,))
            metrics = [dict(row) for row in cur.fetchall()]
            
            # Artifacts
            cur.execute("SELECT * FROM artifacts WHERE run_id=?", (run_id,))
            artifacts = [dict(row) for row in cur.fetchall()]
            
            # Config
            cur.execute("SELECT config_json FROM configs WHERE run_id=?", (run_id,))
            config_row = cur.fetchone()
            config = json.loads(config_row["config_json"]) if config_row else {}
            
            return {
                "run": dict(run_row),
                "metrics": metrics,
                "artifacts": artifacts,
                "config": config
            }
    except sqlite3.OperationalError:
        raise HTTPException(404, "Run not found (DB error)")

@router.get("/{run_id}/diff/{baseline_id}")
def compare_runs(run_id: str, baseline_id: str):
    try:
        with _get_conn() as conn:
            cur = conn.cursor()
            
            cur.execute("SELECT config_json FROM configs WHERE run_id=?", (baseline_id,))
            b_row = cur.fetchone()
            baseline_config = json.loads(b_row["config_json"]) if b_row else {}
            
            cur.execute("SELECT config_json FROM configs WHERE run_id=?", (run_id,))
            r_row = cur.fetchone()
            run_config = json.loads(r_row["config_json"]) if r_row else {}
            
            diff = DiffEngine.compare_configs(baseline_config, run_config)
            return diff
    except sqlite3.OperationalError:
        raise HTTPException(500, "Database error mapping configs")
