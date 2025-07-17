# main.py

from fastapi import FastAPI
from api.routes import router as ideas_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="GitHub Business Idea Generator",
    description="API for generating and serving AI-powered business ideas from GitHub repos.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8081"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ideas_router)
