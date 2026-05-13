from fastapi import FastAPI
from app.core.config import get_settings
from app.routers import courses, recommend, ai, voice
from app.routers import options
from fastapi.middleware.cors import CORSMiddleware

settings = get_settings()

app = FastAPI(title=settings.app_name, version="1.0.0")

app.include_router(courses.router, prefix="/api/courses", tags=["Courses"])
app.include_router(recommend.router, prefix="/api/recommend", tags=["Recommend"])
app.include_router(ai.router, prefix="/api/ai", tags=["AI"])
app.include_router(options.router, prefix="/api/options", tags=["Options"])
app.include_router(voice.router, prefix="/api/voice", tags=["Voice"])

origins = [
    "http://localhost:8501",
    "http://127.0.0.1:8501",
    # 之後部署後再加：
    # "https://你的-streamlit-cloud-run-url.run.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Course AI API is running"}