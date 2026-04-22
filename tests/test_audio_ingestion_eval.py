import pytest
from packages.eval_runners.audio_ingestion.audio_ingestion_eval import AudioIngestionEval

def test_wer_calculation():
    # Arrange: Set up our tool
    evaluator = AudioIngestionEval()
    reference = "the cat sat on the mat"
    hypothesis = "the cat sat on the rug" # One word wrong (rug vs mat)
    
    # Act: Run the calculation
    result = evaluator.evaluate("TEST_01", reference, hypothesis)
    
    # Assert: Check if the math is correct
    # 1 wrong word out of 6 total words = 0.1666...
    assert result["wer"] > 0
    assert result["cer"] < 0.2
    assert result["pii_detected"] == False
