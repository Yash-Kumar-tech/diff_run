from tracker.diff_engine import DiffEngine

def test_basic_diff():
    c1 = {"lr": 0.01, "batch": 32, "model": "v1"}
    c2 = {"lr": 0.05, "batch": 32, "optimizer": "adam"}
    
    diff = DiffEngine.compare_configs(c1, c2)
    assert "optimizer" in diff["added"]
    assert "model" in diff["removed"]
    assert "lr" in diff["changed"]
    assert "batch" not in diff["changed"]
    assert diff["changed"]["lr"]["old"] == 0.01
    assert diff["changed"]["lr"]["new"] == 0.05
    
def test_smart_insights():
    c1 = {"lr": 0.001, "use_aug": False}
    c2 = {"lr": 0.01, "use_aug": True}
    
    diff = DiffEngine.compare_configs(c1, c2)
    insights = diff["insights"]
    assert len(insights) >= 2
    
    types = [i["type"] for i in insights]
    assert "boolean_flip" in types
    assert "large_numeric_increase" in types
