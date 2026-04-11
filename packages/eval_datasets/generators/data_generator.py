import json
from datetime import datetime
from packages.eval_adapters.connections.config import config
import os


class CallMetadata:

    def __init__(self, call_id, scenario, speaker_a, speaker_b, duration_seconds):
        self.call_id = call_id
        self.scenario = scenario
        self.speaker_a = speaker_a
        self.speaker_b = speaker_b
        self.duration_seconds = duration_seconds

    def to_dict(self):
        return {
            "call_id": self.call_id,
            "scenario": self.scenario,
            "speaker_a": self.speaker_a,
            "speaker_b": self.speaker_b,
            "duration_seconds": self.duration_seconds
        }

class CallScript:

    def __init__(self, call_id, scenario):
        self.call_id = call_id
        self.scenario = scenario
        self.turns = []

    def add_turn(self, speaker, text):
        self.turns.append({
            "speaker": speaker,
            "text": text
        })

    def to_dict(self):
        return {
            "call_id": self.call_id,
            "scenario": self.scenario,
            "turns": self.turns
        }

class DataGenerator:

    def __init__(self):
        self.output_path = config["output_path"]
        self.log_path = config["log_path"]
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)

    def save(self, metadata, script):
        record = {
            "generated_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "metadata": metadata.to_dict(),
            "script": script.to_dict()
        }
        try:
            with open(self.output_path, "a") as f:
                f.write(json.dumps(record) + "\n")
                print("saved successfully")
        except Exception as e:
            print(f"Failed to save record: {e}")
            with open(self.log_path, "a") as log:
                log.write(f"{datetime.now().strftime('%Y-%m-%dT%H:%M:%S')} | SAVE_ERROR | {e}\n")

if __name__ == "__main__":

    meta = CallMetadata(
        call_id="CALL_001",
        scenario="balance_enquiry",
        speaker_a="agent",
        speaker_b="customer",
        duration_seconds=120
    )

    script = CallScript(call_id="CALL_001", scenario="balance_enquiry")
    script.add_turn("agent", "Good morning, how can I help you today?")
    script.add_turn("customer", "Hi, I'd like to check my account balance please.")
    script.add_turn("agent", "Of course, can I take your account number?")

    generator = DataGenerator()
    generator.save(meta, script)

