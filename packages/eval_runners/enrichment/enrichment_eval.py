
from packages.eval_runners.base_eval import BaseEval

class EnrichmentEval(BaseEval):
    def __init__(self):
        super().__init__()
        self.stats = {"tp": 0, "fp": 0, "fn": 0, "tn": 0}

    def evaluate(self, call_id, reference_label, hypothesis_label, target_class="vulnerable"):
        """
        Calculates Confusion Matrix stats for a specific high-stakes class.
        Example: target_class='vulnerable'
        """
        ref = reference_label.lower()
        hyp = hypothesis_label.lower()
        
        # Logic to identify TP, FP, FN, TN
        if hyp == target_class and ref == target_class:
            self.stats["tp"] += 1
        elif hyp == target_class and ref != target_class:
            self.stats["fp"] += 1
        elif hyp != target_class and ref == target_class:
            self.stats["fn"] += 1
        else:
            self.stats["tn"] += 1

        # Calculate F1 on the fly
        precision = self.stats["tp"] / (self.stats["tp"] + self.stats["fp"]) if (self.stats["tp"] + self.stats["fp"]) > 0 else 0
        recall = self.stats["tp"] / (self.stats["tp"] + self.stats["fn"]) if (self.stats["tp"] + self.stats["fn"]) > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

        result = {
            "call_id": call_id,
            "metric": "f1_score", # Tells us WHAT the score represents
            "primary_score": round(f1, 4), # The number for the dashboard
            "recall": round(recall, 4),
            "precision": round(precision, 4)
        }
        self.results.append(result)
        return result