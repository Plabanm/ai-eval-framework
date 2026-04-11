from jiwer import wer
from packages.eval_adapters.connections.config import config

class TranscriptionEval:

    def __init__(self):
        self.results = []

    def evaluate(self, call_id, reference, hypothesis):
        score = wer(reference, hypothesis)
        result = {
            "call_id": call_id,
            "reference": reference,
            "hypothesis": hypothesis,
            "wer": round(score, 4)
        }
        self.results.append(result)
        return result


if __name__ == "__main__":

    evaluator = TranscriptionEval()

    result = evaluator.evaluate(
        call_id="CALL_001",
        reference="good morning how can i help you today",
        hypothesis="good morning how can i help you"
    )

    print(result)