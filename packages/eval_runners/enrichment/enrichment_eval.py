from datetime import datetime

from packages.eval_runners.base_eval import BaseEval

class EnrichmentEval(BaseEval):
    def __init__(self):
        super().__init__() # This calls the Parent's __init__ to setup self.results

    def evaluate_sentiment(self, call_id, reference_label, hypothesis_label):
        """Calculates accuracy for a single sentiment prediction."""
        ref = reference_label.strip().lower()
        hyp = hypothesis_label.strip().lower()

        is_correct = (ref == hyp)
        score = 1.0 if is_correct else 0.0
        
        result = {
            "call_id": call_id,
            "metric": "sentiment_accuracy",
            "reference": ref,
            "hypothesis": hyp,
            "score": score
        }
        
        self.results.append(result)
        return result
    
    def evaluate_batch(self, batch_data):
        """
        Processes a list of evaluations.
        batch_data format: [{"id": "1", "ref": "pos", "hyp": "pos"}, ...]
        """
        correct_count = 0
        total_count = len(batch_data)
        
        for item in batch_data:
            res = self.evaluate_sentiment(item["id"], item["ref"], item["hyp"])
            if res["score"] == 1.0:
                correct_count += 1
        
        batch_accuracy = correct_count / total_count if total_count > 0 else 0
        
        summary = {
            "batch_timestamp": datetime.now().isoformat(),
            "total_calls": total_count,
            "accuracy": round(batch_accuracy, 4)
        }
        
        return summary
    
    def calculate_f1(self, tp, fp, fn):
        """Calculates Precision, Recall, and F1-Score."""
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        return {
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1_score": round(f1, 4)
        }

if __name__ == "__main__":
    evaluator = EnrichmentEval()

    # Testing a correct prediction
    res1 = evaluator.evaluate_sentiment("CALL_101", "positive", "positive")
    evaluator.save_results(res1, "enrichment_results.jsonl")

    # Testing an incorrect prediction
    res2 = evaluator.evaluate_sentiment("CALL_102", "negative", "neutral")
    evaluator.save_results(res2, "enrichment_results.jsonl")

    print("Enrichment Eval complete. Check enrichment_results.jsonl!")

    test_batch = [
    {"id": "C1", "ref": "positive", "hyp": "positive"},
    {"id": "C2", "ref": "negative", "hyp": "negative"},
    {"id": "C3", "ref": "neutral", "hyp": "positive"},  # Miss!
    {"id": "C4", "ref": "positive", "hyp": "positive"},
    {"id": "C5", "ref": "negative", "hyp": "positive"}   # Miss!
    ]

    evaluator = EnrichmentEval()
    summary = evaluator.evaluate_batch(test_batch)

    print(f"Batch Summary: {summary}")