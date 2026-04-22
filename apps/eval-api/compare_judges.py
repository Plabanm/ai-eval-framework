from packages.eval_runners.response_synthesis.response_synthesis_eval import ResponseSynthesisEval
import os

def run_comparison():
    judge = ResponseSynthesisEval()
    
    test_data = {
        "call_id": "COMPARE-001",
        "transcript": "Customer wants to cancel their flight from London to New York.",
        "summary": "Customer is flying from Paris to New York."
    }

    # 1. Run Local
    os.environ["EVAL_ENV"] = "local"
    local_res = judge.evaluate(**test_data)
    
    # 2. Run Cloud
    os.environ["EVAL_ENV"] = "prod"
    cloud_res = judge.evaluate(**test_data)

    print(f"\n--- JUDGE COMPARISON ---")
    print(f"Llama 3.2 Score: {local_res['primary_score']} | Reason: {local_res['reason']}")
    print(f"Gemini 3 Score:  {cloud_res['primary_score']} | Reason: {cloud_res['reason']}")

if __name__ == "__main__":
    run_comparison()