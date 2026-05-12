# Course AI API

FastAPI backend service for the 「線上課程智能推薦顧問」 project.

This project provides:

- Course data API
- Course filter API
- Recommendation API
- AI recommendation analysis
- Streamlit frontend integration
- Docker deployment support
- GCP Cloud Run deployment support

---

# Tech Stack

- Python 3.12.13
- FastAPI
- Uvicorn
- Pydantic
- Docker
- Google Gemini API
- LM Studio
- GCP Cloud Run

---

# Project Structure

```bash
course-api/
│
├── app/
│   ├── api/
│   ├── services/
│   ├── models/
│   ├── prompts/
│   ├── utils/
│   ├── data/
│   └── main.py
│
├── requirements.txt
├── Dockerfile
├── .env
└── README.md
```

---

# Create Environment (Optional)

## Conda

```bash
conda create -n your-env-name python=3.12.13

conda activate your-env-name
```

---

## venv

### Windows CMD

```bash
python -m venv venv

venv\Scripts\activate
```

---

### Windows PowerShell

```powershell
python -m venv venv

.\venv\Scripts\Activate.ps1
```

---

### macOS / Linux

```bash
python -m venv venv

source venv/bin/activate
```

---

# Check Python Version

```bash
python -V
```

Expected:

```bash
Python 3.12.13
```

---

# Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Run Local Development Server

```bash
uvicorn app.main:app --reload
```

Default URL:

```bash
http://127.0.0.1:8000
```

Swagger UI:

```bash
http://127.0.0.1:8000/docs
```

---

# API Examples

## Get Schools

```http
GET /api/options/schools
```

Example:

```bash
curl http://127.0.0.1:8000/api/options/schools
```

---

## Get Courses

```http
GET /api/courses
```

---

## Filter Courses

```http
GET /api/courses/filter
```

Example:

```bash
curl "http://127.0.0.1:8000/api/courses/filter?school_id=1&grade_id=11&subject_id=500"
```

---

# Environment Variables

## Gemini

```env
APP_NAME=Course AI API

AI_PROVIDER=gemini
GEMINI_API_KEY=YOUR_API_KEY
GEMINI_MODEL_NAME=gemini-3-flash-preview
```

---

## LM Studio

```env
APP_NAME=Course AI API

AI_PROVIDER=lmstudio
LMSTUDIO_BASE_URL=http://localhost:1234/v1
LMSTUDIO_MODEL_NAME=gemma-3-12b-it
```

---

# Docker Build

```bash
docker build -t course-api:latest .
```

---

# Docker Run

## Use LM Studio

```bash
docker run --rm -p 8000:8080 ^
  -e PORT=8080 ^
  -e APP_NAME="Course AI API" ^
  -e AI_PROVIDER=lmstudio ^
  -e LMSTUDIO_BASE_URL=http://host.docker.internal:1234/v1 ^
  -e LMSTUDIO_MODEL_NAME=gemma-3-12b-it ^
  course-api
```

---

## Use Gemini

```bash
docker run --rm -p 8000:8080 ^
  -e PORT=8080 ^
  -e APP_NAME="Course AI API" ^
  -e AI_PROVIDER=gemini ^
  -e GEMINI_API_KEY=YOUR-KEY ^
  -e GEMINI_MODEL_NAME=gemini-3-flash-preview ^
  course-api
```

---

# GCP Cloud Run Deploy

```bash
gcloud run deploy fastapi-service ^
  --image asia-east1-docker.pkg.dev/YOUR_PROJECT_ID/YOUR_REPOSITORY/course-api:latest ^
  --platform managed ^
  --region asia-east1 ^
  --allow-unauthenticated ^
  --port 8000 ^
  --set-env-vars "APP_NAME=Course AI API,AI_PROVIDER=gemini,GEMINI_MODEL_NAME=gemini-3-flash-preview" ^
  --set-secrets "GEMINI_API_KEY=gemini-key:latest"
```

---

# Features

- Course recommendation API
- AI recommendation analysis
- Dynamic filter options
- Streamlit frontend integration
- Docker support
- Cloud Run deployment
- Gemini AI support
- LM Studio local AI support

---

# Future Plans

- Vector Search integration
- RAG architecture
- Azure AI Search integration
- Azure OpenAI integration
- SQL Database integration
- User behavior analysis
- AI conversation memory
- Recommendation optimization

---

# License

This project is for learning and personal portfolio use.