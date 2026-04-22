import jiwer
from datetime import datetime
from presidio_analyzer import AnalyzerEngine
from packages.eval_runners.base_eval import BaseEval

class AudioIngestionEval(BaseEval):

    def __init__(self):
        super().__init__() # This calls the Parent's __init__ to setup self.results
        self.pii_analyzer = AnalyzerEngine()

    def evaluate(self, call_id, reference, hypothesis):
        """Calculates both WER and CER and returns a full result object."""
        # Standardize to lowercase for fair testing
        ref = reference.lower()
        hyp = hypothesis.lower()

        wer_score = jiwer.wer(ref, hyp)
        cer_score = jiwer.cer(ref, hyp)
        pii_results = self.pii_analyzer.analyze(text=hypothesis, entities=[], language='en')
        pii_found = len(pii_results) > 0

        result = {
            "call_id": call_id,
            "metric": "wer", # Tells us WHAT the score represents
            "primary_score": round(wer_score, 4), # The number for the dashboard
            "reference": reference,
            "hypothesis": hypothesis,
            "wer": round(wer_score, 4),
            "cer": round(cer_score, 4),
            "pii_detected": pii_found,
            "pii_count": len(pii_results),
            "eval_timestamp": datetime.now().isoformat()
        }
        
        self.results.append(result)
        return result
    
    def check_pii(self, text):
        """Returns True if PII is detected, False otherwise."""
        results = self.pii_analyzer.analyze(text=text, entities=[], language='en')
        return len(results) > 0 # If results exist, PII was found!
    

if __name__ == "__main__":
    evaluator = AudioIngestionEval()

    # 1. Run the evaluation
    result = evaluator.evaluate(
        call_id="CALL_001",
        reference="Hello this is a test of the evaluation framework",
        hypothesis="Hello this is a test of the eval framework"
    )

    # 2. Save it to your results file (using your config for the path!)
    # Assuming config.OUTPUT_PATH is defined in your config.py
    evaluator.save_results(result, "audio_ingestion_results.jsonl")

    print(f"Evaluation Complete: {result}")
