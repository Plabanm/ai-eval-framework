import json
from pathlib import Path  # Modern 2026 standard for paths
from datetime import datetime
from packages.eval_adapters.connections.config import ACTIVE_CONFIG

class BaseEval:
    def __init__(self):
        self.results = []
        # Convert string path to a Path object immediately
        raw_path = ACTIVE_CONFIG.get("results_path", "data/results/eval_log.jsonl")
        self.results_path = Path(raw_path)
        
        # .parent gets the folder; .mkdir(parents=True) creates it if missing
        self.results_path.parent.mkdir(parents=True, exist_ok=True)

    def save_results(self, result_data):
        """Standard saving logic with 2026 Audit Metadata."""
        try:
            # 1. Add Essential Metadata for the Dashboard
            result_data["eval_timestamp"] = datetime.now().isoformat()
            
            # 2. Append to JSONL
            # 'a' means append, encoding='utf-8' prevents emoji crashes
            with self.results_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(result_data) + "\n")
            
            # Use a clean debug message
            engine = result_data.get("metadata", {}).get("engine", "unknown")
            print(f"📊 [LOGGED] {result_data['call_id']} | Engine: {engine}")
            
        except Exception as e:
            print(f"❌ Critical Error: Could not write to audit log at {self.results_path}: {e}")