# AI Eval Framework — Claude Code Context

## About This Project

Multi-modal AI eval framework. QA engineer learning Python.
Career goal: AI Quality Lead in 12-18 months.

## Pipeline Being Evaluated

Transcription → Sentiment/Emotion → Punctuation → Relevancy → LLM (Gemini Flash 2.0)

## Repo Structure

- packages/eval-runners/ ← pipeline eval modules (START HERE)
- packages/eval-metrics/ ← WER, CER, toxicity scores
- packages/eval-datasets/ ← JSONL test fixtures (mocked data)
- packages/eval-reporting/ ← per call summaries, regression tracking
- apps/eval-api/ ← FastAPI wrapper
- apps/eval-ui/ ← Streamlit dashboard

## Current Task

Building first eval module: transcription_eval.py in eval-runners
Checks: WER, PII Detection, Hallucination

## Tech Stack

Python · Ollama (local LLM) · RAGAS · Langfuse · FastAPI · Streamlit

## Key Decisions Made

- JSONL for all test fixtures and output logs
- Mock hypothesis/reference data (we don't own the ASR model)
- eval-runners is the first package to build

## Python Level

Beginner+. Knows: functions, venv, Ollama call, basic file handling.
Currently learning: JSONL, classes/OOP next.

## Teaching Style

WHY before HOW. QA analogies. Build real things only.

## The 4 Services We Evaluate

1. Transcription (Parakeet) — WAV → word-level JSON
2. Metadata Enrichment (spaCy + RoBERTa) — JSON → enriched JSON
3. Call Relevancy (MiniLM) — enriched JSON → relevancy JSON
4. OnDemand LLM (Gemini Flash 2.0) — enriched JSON → summary + RAG answers

## Data Strategy

- DEV: synthetic WAV via TTS → mock JSON → eval
- PROD: real WAV → real model → real JSON → eval
- Data generators live in: packages/eval-datasets/generators/

## Next Task

Build packages/eval-datasets/generators/data_generator.py
Then: packages/eval-runners/transcription_eval.py
