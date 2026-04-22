import os
from dotenv import load_dotenv

load_dotenv()

# THE MISSING PIECE: Ensure these are defined at the top level
EVAL_ENV = os.getenv("EVAL_ENV", "local")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Thresholds
QUALITY_THRESHOLDS = {
    "max_wer": 0.15,
    "min_accuracy": 1.0,
    "min_llm_score": 0.8
}

if EVAL_ENV == "local":
    ACTIVE_CONFIG = {
        "llm_model": "llama3.2",
        "results_path": "data/results/local_run.jsonl"
    }
else:
    ACTIVE_CONFIG = {
        "llm_model": "gemini-3-flash-preview",
        "results_path": "data/results/prod_run.jsonl"
    }

# config.py
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

ACTIVE_CONFIG = {
    "results_path": os.path.join(BASE_DIR, "data/results/prod_run.jsonl")
}    