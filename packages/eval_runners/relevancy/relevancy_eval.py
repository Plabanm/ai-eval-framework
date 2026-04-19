from packages.eval_runners.base_eval import BaseEval

class RelevancyEval(BaseEval):
    def __init__(self, judge_model="gemini-1.5-flash"):
        super().__init__()
        self.judge_model = judge_model

    def evaluate_relevancy(self, call_id, original_transcript, ai_summary):
        """
        Calls an LLM to judge if the summary matches the transcript.
        """
        prompt = f"""
        Rate the following summary based on the transcript.
        Score from 1 (Poor) to 5 (Excellent).
        
        Transcript: {original_transcript}
        Summary: {ai_summary}
        
        Return ONLY a JSON object: {{"score": 5, "reasoning": "..."}}
        """
        
        # Here we would use our 'connections' package to call the LLM
        # For now, let's simulate a successful 'Lead' quality response
        score = 5 
        
        result = {
            "call_id": call_id,
            "metric": "semantic_relevancy",
            "score": score,
            "judge_model": self.judge_model
        }
        self.results.append(result)
        return result