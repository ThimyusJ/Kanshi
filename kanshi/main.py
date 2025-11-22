# main.py

from fastapi import FastAPI
from kanshi_api import router as kanshi_api

app = FastAPI(
    title="Kai Core – Multi-Agent API",
    description="Unified HTTP interface for Kanshi and future agents.",
    version="0.1.0",
)

# Register Kanshi's API subrouter
app.include_router(kanshi_api)
