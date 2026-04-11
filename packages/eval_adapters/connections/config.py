import os

ENVIRONMENT = os.getenv("EVAL_ENV", "local")

if ENVIRONMENT == "local":
    config = {
        "transcription_model": "whisper",
        "llm_model": "llama3.2",
        "output_path": "data/output/call_data.jsonl",
        "log_path": "data/logs/errors.log",
    }
elif ENVIRONMENT == "prod":
    config = {
        "transcription_model": "parakeet",
        "llm_model": "gemini-flash-2.0",
        "output_path": "/prod/data/call_data.jsonl",
        "log_path": "/prod/logs/errors.log"
    }
else:
    raise ValueError(f"Unknown environment: {ENVIRONMENT}")
