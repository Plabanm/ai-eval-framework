from jiwer import wer
import jiwer
import json
from datetime import datetime
from packages.eval_adapters.connections.config import config
from packages.eval_runners.base_eval import BaseEval

class TranscriptionEval(BaseEval):

    def __init__(self):
        super().__init__() # This calls the Parent's __init__ to setup self.results

    def evaluate(self, call_id, reference, hypothesis):
        """Calculates both WER and CER and returns a full result object."""
        # Standardize to lowercase for fair testing
        ref = reference.lower()
        hyp = hypothesis.lower()

        wer_score = jiwer.wer(ref, hyp)
        cer_score = jiwer.cer(ref, hyp)

        result = {
            "call_id": call_id,
            "reference": reference,
            "hypothesis": hypothesis,
            "wer": round(wer_score, 4),
            "cer": round(cer_score, 4),
            "eval_timestamp": datetime.now().isoformat()
        }
        
        self.results.append(result)
        return result
    

if __name__ == "__main__":
    evaluator = TranscriptionEval()

    # 1. Run the evaluation
    result = evaluator.evaluate(
        call_id="CALL_001",
        reference="Hello this is a test of the evaluation framework",
        hypothesis="Hello this is a test of the eval framework"
    )

    # 2. Save it to your results file (using your config for the path!)
    # Assuming config.OUTPUT_PATH is defined in your config.py
    evaluator.save_results(result, "transcription_results.jsonl")

    print(f"Evaluation Complete: {result}")