import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from backend.app.config import get_settings
from backend.app.api.upload import router as upload_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("finance_app")

settings = get_settings()

app = FastAPI(
    title="Personal Finance Intelligence API",
    description="Finance analysis, behavior detection, rule-based recommendations & AI insights",
    version="1.0.0",
)

# CORS setup
origins = settings.cors_origins_list or ["http://localhost:5173", "http://127.0.0.1:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all during local development for easy access
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(upload_router)


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Personal Finance Intelligence API",
        "configured_ai_provider": settings.AI_PROVIDER,
        "has_groq_key": bool(settings.GROQ_API_KEY),
        "has_grok_key": bool(settings.XAI_API_KEY),
    }


@app.get("/")
def root():
    return {
        "message": "Personal Finance Intelligence & Recommendation System API",
        "documentation": "/docs",
        "health": "/api/health",
    }

