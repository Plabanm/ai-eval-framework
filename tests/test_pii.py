import pytest
from packages.eval_runners.audio_ingestion.audio_ingestion_eval import AudioIngestionEval

def test_pii_detection_catches_phone_number():
    # Arrange
    evaluator = AudioIngestionEval()
    # An audio-ingestion result where the AI forgot to redact a UK mobile number
    leaked_transcript = "The customer called from 07700 900123 to complain."
    
    # Act
    result = evaluator.evaluate("CALL_PII_01", "REFERENCE_IGNORED", leaked_transcript)
    
    # Assert
    assert result["pii_detected"] is True
    assert result["pii_count"] > 0
    print(f"✅ Successfully caught {result['pii_count']} PII entities.")

def test_clean_transcript_has_no_pii():
    # Arrange
    evaluator = AudioIngestionEval()
    clean_transcript = "The customer wanted to talk about their billing cycle."
    
    # Act
    result = evaluator.evaluate("CALL_CLEAN_01", "REF", clean_transcript)
    
    # Assert
    assert result["pii_detected"] is False
