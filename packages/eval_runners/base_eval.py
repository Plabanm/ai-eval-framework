import json
from datetime import datetime

class BaseEval:
    def __init__(self):
        self.results = []

    def save_results(self, result_data, output_path):
        """Standard saving logic for all evaluation services."""
        try:
            if "eval_timestamp" not in result_data:
                result_data["eval_timestamp"] = datetime.now().isoformat()
            
            with open(output_path, "a") as f:
                f.write(json.dumps(result_data) + "\n")
            print(f"✅ Result saved to {output_path}")
        except Exception as e:
            print(f"❌ Failed to save result: {e}")