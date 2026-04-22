from packages.eval_runners.base_eval import BaseEval

class RouteJudgeEval(BaseEval):
    def evaluate(self, call_id, reference, hypothesis):
        """
        In RouteJudge:
        - reference = The 'True' Journey (e.g., 'Mortgage')
        - hypothesis = The AI's Predicted Journey
        """
        # 1. Core Logic: Check for a match
        # We use .strip().lower() to handle 'Mortgage' vs 'mortgage '
        is_match = reference.strip().lower() == hypothesis.strip().lower()
        score = 1.0 if is_match else 0.0
        
        result = {
            "call_id": call_id,
            "metric": "accuracy",
            "primary_score": score,
            "reference": reference,
            "hypothesis": hypothesis,
            "reason": "Exact match" if is_match else f"Mismatched journey: expected {reference}"
        }
        
        self.results.append(result)
        return result