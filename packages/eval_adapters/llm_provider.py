import requests
from packages.eval_adapters.connections.config import config, EVAL_MODE, GEMINI_API_KEY, OLLAMA_BASE_URL

def call_llm_judge(prompt: str):
    if EVAL_MODE == "local":
        # Call Ollama
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={"model": config["llm_model"], "prompt": prompt, "stream": False}
        )
        return response.json().get("response")
    else:
        # Placeholder for Gemini API call
        # return call_gemini_api(prompt, GEMINI_API_KEY)
        return "0.85" # Mocking for now