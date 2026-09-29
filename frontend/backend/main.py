
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes import router

app = FastAPI(
    title="LegalEase API",
    description="AI-Powered Legal Document Generator",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(router)


@app.get("/")
def home():
    return {
        "name": "LegalEase API",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
def health():

    from backend.ai_core.gemini_generator import (
        GeminiDocumentGenerator
    )

    generator = GeminiDocumentGenerator()

    return {
        "status": "healthy",
        "gemini_configured": generator.configured,
        "model": generator.model
    }