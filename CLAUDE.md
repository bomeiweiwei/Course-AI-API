# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

**Install dependencies:**
```bash
pip install -r requirements.txt
```

**Run development server:**
```bash
uvicorn app.main:app --reload
```
API available at http://127.0.0.1:8000, Swagger UI at http://127.0.0.1:8000/docs

**Docker build and run:**
```bash
docker build -t course-api:latest .

# With Gemini:
docker run --rm -p 8000:8080 -e PORT=8080 -e AI_PROVIDER=gemini -e GEMINI_API_KEY=YOUR-KEY course-api

# With LM Studio:
docker run --rm -p 8000:8080 -e PORT=8080 -e AI_PROVIDER=lmstudio -e LMSTUDIO_BASE_URL=http://host.docker.internal:1234/v1 course-api
```

No test or lint tooling is currently configured.

## Architecture

This is a FastAPI backend for an intelligent online course recommendation system (線上課程智能推薦顧問). Data is served from JSON files (no database).

### Request Flow

```
Router → Service → (AI Layer | Data Layer)
```

- **Routers** (`app/routers/`): Thin HTTP handlers delegating to services
- **Services** (`app/services/`): Business logic — filtering, scoring, AI orchestration
- **AI Layer** (`app/ai/`): LangChain-based abstraction over Gemini and LM Studio
- **Data** (`app/data/`): `courses.json` (course catalog) and `options.json` (hierarchical metadata for dropdowns)

### Recommendation Pipeline

1. Filter courses from `courses.json` by `school_id`, `grade_id`, `subject_id` (required) and optional `version_id`, `degree_id`, `goal_id`
2. Score each course: rating×10 + enrollment bonus (0–20) + budget alignment (0–20) + preference match (0–5 per match)
3. Return top N results (default 3, max 10) with a `reason` string
4. Optionally call AI via `POST /api/ai/course/recommendation` to generate a natural-language recommendation explanation

### AI Provider Abstraction

`app/ai/factory.py` creates an AI client based on `AI_PROVIDER` env var:
- `gemini` → `GeminiClient` (wraps `ChatGoogleGenerativeAI` via LangChain)
- `lmstudio` → `LmStudioClient` (wraps `ChatOpenAI` pointed at local LM Studio endpoint)

Both share the `BaseAILangchain` interface with `invoke()` and `chat()` methods.

Voice-to-text (`app/services/voice_service.py`) uses the `google-genai` SDK directly (not LangChain) to upload audio to Gemini Files API and transcribe to Traditional Chinese.

### Prompts

`app/prompts/recommend_prompt_builder.py` builds structured prompts for AI recommendation explanations. `app/knowledge/textbook_knowledge.py` provides curated textbook descriptions injected into prompts via `app/services/textbook_service.py`.

## Environment Variables

Copy `.env.example` to `.env`. Key variables:

| Variable | Default | Notes |
|---|---|---|
| `AI_PROVIDER` | `lmstudio` | `gemini` or `lmstudio` |
| `GEMINI_API_KEY` | — | Required when using Gemini |
| `GEMINI_MODEL_NAME` | `gemini-1.5-flash` | Gemini model ID |
| `LMSTUDIO_BASE_URL` | `http://localhost:1234/v1` | LM Studio OpenAI-compatible endpoint |
| `LMSTUDIO_MODEL_NAME` | `local-model` | Model name as shown in LM Studio |

Settings are loaded via Pydantic Settings in `app/core/config.py` with LRU caching (`get_settings()`).

## Deployment

Targets GCP Cloud Run. The `PORT` env var controls the uvicorn port (defaults to 8080 in Docker). The `feature/cloud` branch contains ongoing cloud infrastructure work; `develop` is the main integration branch.
