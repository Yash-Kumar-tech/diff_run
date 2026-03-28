import os
import subprocess
from typing import Any, Dict, Optional

from .storage.sqlite_store import SQLiteStore
from .storage.file_store import FileStore

class Experiment:
    """Main interface for logging ML experiments locally."""
    
    def __init__(self, project_name: str, db_path: str = "./.diff_run/tracker.db", artifacts_dir: str = "./.diff_run/artifacts"):
        self.project_name = project_name
        self._setup_dirs(db_path, artifacts_dir)
        
        self.db = SQLiteStore(db_path)
        self.file_store = FileStore(artifacts_dir)
        
        env_info = self._capture_environment()
        self.run_id = self.db.create_run(self.project_name, env_info)
        
    def _setup_dirs(self, db_path: str, artifacts_dir: str):
        if os.path.dirname(db_path):
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
        os.makedirs(artifacts_dir, exist_ok=True)
        
    def _capture_environment(self) -> Dict[str, Any]:
        """Capture git commit and dirty state."""
        env_info = {
            "git_commit": "unknown",
            "is_dirty": False
        }
        try:
            # Check git commit
            commit_res = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=False)
            if commit_res.returncode == 0:
                env_info["git_commit"] = commit_res.stdout.strip()
            
            # Check dirty state
            dirty_res = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, check=False)
            if dirty_res.returncode == 0:
                env_info["is_dirty"] = len(dirty_res.stdout.strip()) > 0
                
        except Exception:
            pass
            
        return env_info

    def log_metric(self, name: str, value: float, step: Optional[int] = None):
        """Log a scalar metric."""
        self.db.log_metric(self.run_id, name, float(value), step)
        
    def log_config(self, config: Dict[str, Any]):
        """Log experiment hyperparameters/configuration."""
        self.db.log_config(self.run_id, config)
        
    def log_image(self, name: str, image_array, step: Optional[int] = None):
        """Log an image artifact."""
        path = self.file_store.save_image(self.run_id, name, image_array, step)
        self.db.log_artifact(self.run_id, "image", name, path)
        
    def log_audio(self, name: str, audio_waveform, sample_rate: int, step: Optional[int] = None):
        """Log an audio artifact."""
        path = self.file_store.save_audio(self.run_id, name, audio_waveform, sample_rate, step)
        self.db.log_artifact(self.run_id, "audio", name, path)
        
    def log_system_metrics(self, step: Optional[int] = None):
        """Logs CPU and Memory usage if psutil is installed."""
        try:
            import psutil
            cpu = psutil.cpu_percent(interval=None)
            mem = psutil.virtual_memory().percent
            self.log_metric("sys_cpu_percent", cpu, step)
            self.log_metric("sys_mem_percent", mem, step)
        except ImportError:
            pass
