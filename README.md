# AI Eval Framework

A modular, multi-modal evaluation framework for LLM pipelines.

## Pipeline

Transcription → Sentiment/Emotion → Punctuation → Relevancy → LLM Judge

## Structure

- `packages/eval-runners/` — pipeline eval modules
- `packages/eval-metrics/` — scoring (WER, BLEU, custom)
- `packages/eval-datasets/` — JSONL test datasets
- `packages/eval-reporting/` — output reports
- `apps/eval-api/` — FastAPI wrapper
- `apps/eval-ui/` — Streamlit dashboard

## Tech Stack

Python · Ollama · RAGAS · Langfuse · FastAPI · Streamlit
