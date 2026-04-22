import requests
from google import genai
import json
from packages.eval_runners.base_eval import BaseEval
from packages.eval_adapters.connections.config import ACTIVE_CONFIG, EVAL_ENV, OLLAMA_BASE_URL, GEMINI_API_KEY

class ResponseSynthesisEval(BaseEval):
    def evaluate(self, call_id, transcript=None, summary=None, **kwargs):
        # 1. Initialize variables at the top to avoid UnboundLocalError
        score = 0.0
        reason = "Evaluation not performed."
        cost = 0.0 
        
        if not transcript or not summary:
            return {
                "call_id": call_id,
                "metric": "llm_faithfulness",
                "primary_score": 0.0,
                "reason": "Missing transcript or summary data for evaluation."
            }

        prompt = f"""
        Evaluate the following summary based on the transcript.
        Transcript: {transcript}
        Summary: {summary}
        Return ONLY a JSON object: {{"score": <float>, "reason": "<string>"}}
        """

        try:
            if EVAL_ENV == "local":
                endpoint = f"{OLLAMA_BASE_URL}/api/generate"
                payload = {
                    "model": ACTIVE_CONFIG["llm_model"],
                    "prompt": prompt,
                    "stream": False,
                    "format": "json"
                }
                response = requests.post(endpoint, json=payload)
                response.raise_for_status() # Check for HTTP errors
                raw_output = response.json().get("response")
                cost = 0.0 
            else:
                client = genai.Client(api_key=GEMINI_API_KEY)
                response = client.models.generate_content(
                    model=ACTIVE_CONFIG["llm_model"],
                    contents=prompt,
                    config={'response_mime_type': 'application/json'}
                )

                usage = response.usage_metadata
                cost = ((usage.prompt_token_count / 1_000_000) * 0.10) + \
                       ((usage.candidates_token_count / 1_000_000) * 0.40)
                
                print(f"--- [CLOUD EVAL] {call_id} | Cost: ${cost:.6f} ---")
                raw_output = response.text
            
            judge_data = json.loads(raw_output)
            score = judge_data.get("score", 0.0)
            reason = judge_data.get("reason", "No reason provided by model.")
            
        except Exception as e:
            # Score and cost remain 0.0 as initialized above
            reason = f"LLM Judge Error: {str(e)}"

        result = {
            "call_id": call_id,
            "metric": "llm_faithfulness",
            "primary_score": score,
            "reason": reason,
            "metadata": {
                "engine": ACTIVE_CONFIG["llm_model"],
                "environment": EVAL_ENV,
                "eval_cost": cost 
            }
        }
        self.results.append(result)
        self.save_results(result)
        return result