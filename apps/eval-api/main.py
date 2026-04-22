from typing import List, Optional
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from packages.eval_runners.registry import get_evaluator

app = FastAPI(title="AI Quality Assurance Platform")

# Define what a 'Request' looks like
class EvalRequest(BaseModel):
    call_id: str
    reference: Optional[str] = None   # Used for Services 1-3
    hypothesis: Optional[str] = None  # Used for Services 1-3
    transcript: Optional[str] = None  # Used for Service 4
    summary: Optional[str] = None     # Used for Service 4

@app.post("/evaluate/{service_name}")
def trigger_evaluation(service_name: str, request: EvalRequest):
    runner = get_evaluator(service_name)
    
    # We pull the data out of the 'request' object
    # result = runner.evaluate(
    #     call_id=request.call_id, 
    #     reference=request.reference, 
    #     hypothesis=request.hypothesis
    # )
    data = request.model_dump()
    result = runner.evaluate(**data)
    return result

# New Batch Endpoint
@app.post("/evaluate/batch/{service_name}")
def trigger_batch_evaluation(service_name: str, requests: List[EvalRequest]):
    """
    Accepts a list of calls and returns a summarized evaluation.
    """
    runner = get_evaluator(service_name)
    
    # 1. Convert incoming Pydantic list to a list of dicts, then to a DataFrame
    data = [req.dict() for req in requests]
    df = pd.DataFrame(data)
    
    # 2. Run evaluations (Using the lead logic we wrote in previous sessions)
    all_results = []
    for _, row in df.iterrows():
        res = runner.evaluate(row['call_id'], row['reference'], row['hypothesis'])
        all_results.append(res)
    
    # 3. Create a summary using Pandas Vectorization
    results_df = pd.DataFrame(all_results)
    summary = {
        "total_processed": len(results_df),
        "average_score": float(results_df['primary_score'].mean()), # Lead move: .mean()
        "failures": int((results_df['primary_score'] < 0.5).sum())
    }
    
    return {
        "summary": summary,
        "detailed_results": all_results
    }