# Course AI API

## Environment

- Python 3.12+
- FastAPI
- Uvicorn

---

## Install

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create `.env` from `.env.example`

```bash
copy .env.example .env
```

Example `.env.example`

```env
APP_NAME=Course AI API

AI_PROVIDER=lmstudio

GEMINI_API_KEY=
GEMINI_MODEL_NAME=gemini-1.5-flash

LMSTUDIO_BASE_URL=http://localhost:1234/v1
LMSTUDIO_MODEL_NAME=local-model

AZURE_OPENAI_API_KEY=
AZURE_OPENAI_ENDPOINT=
```

---

## Run

```bash
uvicorn app.main:app --reload
```

---

## Swagger API Docs

```text
http://127.0.0.1:8000/docs
```

---

## Project Structure

```text
course-ai-api/
│
├── app/
│   ├── ai/
│   ├── core/
│   ├── data/
│   ├── models/
│   ├── prompts/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   └── main.py
│
├── .env
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

---

## API Routes

### Root

```text
GET /
```

### Course

```text
GET /api/courses
GET /api/courses/filter
```

### Recommend

```text
POST /api/recommend
```

### Options

```text
GET /api/options
GET /api/options/schools
GET /api/options/grades
GET /api/options/subjects
GET /api/options/versions
GET /api/options/degrees
GET /api/options/goals
GET /api/options/preferences
```

---

## API Example

### Get Schools

```text
GET /api/options/schools
```

### Get Grades

```text
GET /api/options/grades?school_id=1
```

### Get Subjects

```text
GET /api/options/subjects?grade_id=11
```

### Get Versions

```text
GET /api/options/versions?subject_id=500
```

### Get Courses

```text
GET /api/courses
```

### Filter Courses

```text
GET /api/courses/filter?school_id=1&grade_id=11
```

### Recommend

```text
POST /api/recommend
```

```json
{
  "school_id": 1,
  "grade_id": 11,
  "subject_id": 500,
  "version_id": 1000,
  "degree_id": 2,
  "goal_id": 3,
  "preference_ids": [1, 2],
  "limit": 5
}
```

---

## Notes

- JSON is currently used as mock data source
- Backend framework uses FastAPI
- Frontend integration planned with Streamlit