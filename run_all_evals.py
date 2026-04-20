from packages.eval_core.dataset_registry import DatasetRegistry
from packages.eval_runners.registry import get_evaluator

def run_enterprise_eval():
    # 1. Initialize our Data 'Plumbing'
    registry = DatasetRegistry(data_path="data/results")
    
    # 2. Load Service 1 (Transcription) results to see what needs more work
    transcription_df = registry.get_service_df("transcription")
    
    # 3. We only want to run Enrichment eval on calls that passed Transcription PII check
    clean_calls = transcription_df[transcription_df['pii_detected'] == False]
    
    print(f"🚀 Found {len(clean_calls)} clean calls to process for Enrichment.")

    # 4. Run the next service in the pipeline
    enrichment_runner = get_evaluator("enrichment")
    
    for index, row in clean_calls.iterrows():
        # Using row data to feed the next eval
        result = enrichment_runner.evaluate(
            call_id=row['call_id'],
            reference_label="positive", # Usually from your 'Golden' dataset
            hypothesis_label="positive"  # This would come from your real Service 2 output
        )
        print(f"Processed Call {row['call_id']}: F1 Score {result['primary_score']}")

if __name__ == "__main__":
    run_enterprise_eval()