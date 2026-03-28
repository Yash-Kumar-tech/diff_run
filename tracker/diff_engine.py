from typing import Any, Dict, List

class DiffInsight:
    def __init__(self, key: str, insight_type: str, message: str):
        self.key = key
        self.type = insight_type
        self.message = message
        
    def to_dict(self):
        return {"key": self.key, "type": self.type, "message": self.message}

class DiffEngine:
    @staticmethod
    def compare_configs(config1: Dict[str, Any], config2: Dict[str, Any]) -> Dict[str, Any]:
        """Compares config1 (old/baseline) to config2 (new)."""
        added = {}
        removed = {}
        changed = {}
        insights = []
        
        c1_keys = set(config1.keys())
        c2_keys = set(config2.keys())
        
        for k in c2_keys - c1_keys:
            added[k] = config2[k]
        
        for k in c1_keys - c2_keys:
            removed[k] = config1[k]
            
        for k in c1_keys.intersection(c2_keys):
            v1 = config1[k]
            v2 = config2[k]
            if v1 != v2:
                changed[k] = {"old": v1, "new": v2}
                
                # Smart Insights
                if isinstance(v1, bool) and isinstance(v2, bool):
                    insights.append(DiffInsight(k, "boolean_flip", f"'{k}' flipped from {v1} to {v2}"))
                elif isinstance(v1, (int, float)) and isinstance(v2, (int, float)):
                    if v1 != 0:
                        ratio = v2 / v1
                        if ratio >= 10:
                            insights.append(DiffInsight(k, "large_numeric_increase", f"'{k}' increased >= 10x (from {v1} to {v2})"))
                        elif ratio <= 0.1:
                            insights.append(DiffInsight(k, "large_numeric_decrease", f"'{k}' decreased >= 10x (from {v1} to {v2})"))
                            
        return {
            "added": added,
            "removed": removed,
            "changed": changed,
            "insights": [i.to_dict() for i in insights]
        }
