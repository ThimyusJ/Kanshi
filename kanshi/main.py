# main.py

from fastapi import FastAPI
from kanshi_api import router as kanshi_api
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Kai Core – Multi-Agent API",
    description="Unified HTTP interface for Kanshi and future agents.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Register Kanshi's API subrouter
app.include_router(kanshi_api)
