import sqlite3
import json
import uuid
from datetime import datetime
from typing import Any, Dict, Optional
from .base import BaseStorage

class SQLiteStore(BaseStorage):
    def __init__(self, db_path: str = "diff_run.db"):
        self.db_path = db_path
        self._init_db()

    def _get_conn(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        with self._get_conn() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS runs (
                    id TEXT PRIMARY KEY,
                    project TEXT,
                    status TEXT,
                    start_time TIMESTAMP,
                    git_commit TEXT,
                    env_hash TEXT,
                    is_dirty BOOLEAN
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    run_id TEXT,
                    step INTEGER,
                    name TEXT,
                    value REAL,
                    timestamp TIMESTAMP,
                    FOREIGN KEY(run_id) REFERENCES runs(id)
                )
            ''')
            # For simplistic diffing, we can store full config as JSON per run.
            conn.execute('''
                CREATE TABLE IF NOT EXISTS configs (
                    run_id TEXT PRIMARY KEY,
                    config_json TEXT,
                    FOREIGN KEY(run_id) REFERENCES runs(id)
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS artifacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    run_id TEXT,
                    type TEXT,
                    name TEXT,
                    file_path TEXT,
                    FOREIGN KEY(run_id) REFERENCES runs(id)
                )
            ''')
            
    def create_run(self, project: str, env_info: Dict[str, Any]) -> str:
        run_id = str(uuid.uuid4())
        start_time = datetime.utcnow().isoformat()
        git_commit = env_info.get("git_commit", "unknown")
        # Ensure we convert boolean to int since SQLite handles bools as 0/1
        is_dirty = 1 if env_info.get("is_dirty", False) else 0
        
        with self._get_conn() as conn:
            conn.execute(
                "INSERT INTO runs (id, project, status, start_time, git_commit, is_dirty) VALUES (?, ?, ?, ?, ?, ?)",
                (run_id, project, "running", start_time, git_commit, is_dirty)
            )
        return run_id

    def log_metric(self, run_id: str, name: str, value: float, step: Optional[int] = None):
        timestamp = datetime.utcnow().isoformat()
        with self._get_conn() as conn:
            conn.execute(
                "INSERT INTO metrics (run_id, step, name, value, timestamp) VALUES (?, ?, ?, ?, ?)",
                (run_id, step, name, value, timestamp)
            )

    def log_config(self, run_id: str, config: Dict[str, Any]):
        # Using REPLACE which acts as upsert if PK exists.
        config_json = json.dumps(config)
        with self._get_conn() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO configs (run_id, config_json) VALUES (?, ?)",
                (run_id, config_json)
            )

    def log_artifact(self, run_id: str, artifact_type: str, name: str, file_path: str):
        with self._get_conn() as conn:
            conn.execute(
                "INSERT INTO artifacts (run_id, type, name, file_path) VALUES (?, ?, ?, ?)",
                (run_id, artifact_type, name, file_path)
            )
