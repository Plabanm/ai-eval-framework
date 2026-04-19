import pytest
from packages.eval_runners.transcription.transcription_eval import TranscriptionEval

def test_transcription_perfect_match():
    evaluator = TranscriptionEval()
    result = evaluator.evaluate(
        call_id="TEST_001",
        reference="This is a perfect test",
        hypothesis="This is a perfect test"
    )
    
    # These are your 'Quality Gates'
    assert result["wer"] == 0.0
    assert result["cer"] == 0.0

def test_transcription_case_insensitivity():
    evaluator = TranscriptionEval()
    # If your code is good, "HELLO" and "hello" should have 0 error
    result = evaluator.evaluate(
        call_id="TEST_002",
        reference="HELLO WORLD",
        hypothesis="hello world"
    )
    
    assert result["wer"] == 0.0