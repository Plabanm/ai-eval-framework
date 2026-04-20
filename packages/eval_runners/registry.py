from packages.eval_runners.transcription.transcription_eval import TranscriptionEval
from packages.eval_runners.enrichment.enrichment_eval import EnrichmentEval

# The "Brain" of the framework
EVALUATOR_REGISTRY = {
    "transcription": TranscriptionEval,
    "enrichment": EnrichmentEval
}

def get_evaluator(service_name):
    """Factory function to fetch the correct evaluator."""
    eval_class = EVALUATOR_REGISTRY.get(service_name.lower())
    if not eval_class:
        raise ValueError(f"Service '{service_name}' not supported!")
    return eval_class()