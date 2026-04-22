import pandas as pd
import json

class DatasetRegistry:
    def __init__(self, data_path="data/results"):
        self.data_path = data_path

    def get_service_df(self, service_name):
        """Loads a JSONL file into a Pandas DataFrame."""
        file_path = f"{self.data_path}/{service_name}_results.jsonl"
        # We use 'lines=True' because we chose JSONL (JSON Lines) format
        return pd.read_json(file_path, lines=True)

    def filter_high_risk(self, df):
        """Isolate the high-stakes data."""
        # Check for PII leaks or low confidence
        return df[(df['pii_detected'] == True) | (df['wer'] > 0.5)]
    
    def join_evals(self, df_a, df_b, join_on="call_id"):
        """
        Combines results from two services (e.g., ASR and Enrichment) 
        so we can see how ASR errors impact Sentiment accuracy.
        """
        return pd.merge(df_a, df_b, on=join_on, suffixes=('_asr', '_enrich'))