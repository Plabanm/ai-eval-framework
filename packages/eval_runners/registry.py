from packages.eval_runners.audio_ingestion.audio_ingestion_eval import AudioIngestionEval
from packages.eval_runners.response_synthesis.response_synthesis_eval import ResponseSynthesisEval
from packages.eval_runners.semantic_enrichment.semantic_enrichment_eval import SemanticEnrichmentEval
from packages.eval_runners.route_judge.route_judge_eval import RouteJudgeEval

# The "Brain" of the framework
EVALUATOR_REGISTRY = {
    "audio_ingestion": AudioIngestionEval,
    "semantic_enrichment": SemanticEnrichmentEval,
    "route_judge": RouteJudgeEval,
    "response_synthesis": ResponseSynthesisEval,  # <--- Add this line!
    
    # Aliases
    "transcription": AudioIngestionEval,
    "enrichment": SemanticEnrichmentEval,
    "relevancy": RouteJudgeEval,
    "summarization": ResponseSynthesisEval,       # <--- Professional alias
}

def get_evaluator(service_name):
    """Factory function to fetch the correct evaluator."""
    eval_class = EVALUATOR_REGISTRY.get(service_name.lower())
    if not eval_class:
        raise ValueError(f"Service '{service_name}' not supported!")
    return eval_class()
