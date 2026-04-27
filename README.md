# Humanizer Lab

Humanizer Lab is an original, transparent framework for converting AI-generated writing into more humanized text.

## Features

- Rule-based learning from paired examples (`AI -> Humanized`)
- Explainable rule extraction with confidence and evidence
- Rule bank merging, provenance, and enable/disable controls
- Conversion modes: rule-only, AI, hybrid (default)
- Heuristic scoring and optional model-based scoring
- FastAPI backend + React frontend
- CLI for workflows and automation

## Project Structure

- `src/humanizer_lab/`: core engine
- `backend/`: API service
- `frontend/`: UI
- `config/model_config.json`: model configuration
- `data/`: examples and persisted rule bank
- `tests/`: unit tests

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

## Model Configuration

Edit `config/model_config.json` and/or environment variables:

```bash
export MODEL_BASE_URL="https://api.example.com/v1"
export MODEL_API_KEY="..."
export MODEL_ID="gpt-4.1-mini"
```

Priority order: `ENV > config/model_config.json`.

## Run Backend

```bash
uvicorn backend.app:app --reload
```

## Run Frontend

```bash
cd frontend
npm install
npm run dev
```

## API Endpoints

- `POST /api/humanize`
- `POST /api/analyze-pair`
- `POST /api/score`
- `GET /api/rules`
- `POST /api/rules/update`
- `GET /api/config`
- `POST /api/config`
- `POST /api/test-model`

## CLI

```bash
add-example --ai-text "..." --human-text "..."
analyze-pair --ai-text "..." --human-text "..."
humanize --text "..." --mode hybrid
score --text "..."
export-prompt
```

## Example Workflow

1. Add training pairs in UI (Train Framework tab) or CLI.
2. Analyze pair and inspect extracted rules.
3. Merge/update rule bank.
4. Humanize new text in hybrid mode.
5. Compare scores before/after and inspect rule trace.

## Limitations

- Heuristic scoring is not a definitive AI detector.
- Rule-only rewriting uses deterministic text transforms and may be conservative.
- AI scoring quality depends on external model behavior.
- Human review is still recommended for high-stakes content.
