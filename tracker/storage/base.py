import abc
from typing import Any, Dict, Optional

class BaseStorage(abc.ABC):
    """Abstract interface for experiment metadata and metric storage."""
    
    @abc.abstractmethod
    def create_run(self, project: str, env_info: Dict[str, Any]) -> str:
        """Create a new run and return its unique ID."""
        pass
        
    @abc.abstractmethod
    def log_metric(self, run_id: str, name: str, value: float, step: Optional[int] = None):
        """Log a numerical metric."""
        pass
        
    @abc.abstractmethod
    def log_config(self, run_id: str, config: Dict[str, Any]):
        """Log configuration as key-values or a single JSON object."""
        pass
        
    @abc.abstractmethod
    def log_artifact(self, run_id: str, artifact_type: str, name: str, file_path: str):
        """Log the metadata (e.g., path) of a saved media artifact."""
        pass
