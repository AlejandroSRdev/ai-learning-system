import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.database import engine
from src.api.routes import students, explain, evaluate, correct

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        async with engine.begin() as conn:
            await conn.run_sync(lambda _: None)
    except Exception:
        logger.critical("Startup failed: database connection could not be established.")
        raise
    yield


app = FastAPI(lifespan=lifespan)

FRONTEND_URL = os.getenv("FRONTEND_URL")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL] if FRONTEND_URL else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(students.router, prefix="/students", tags=["students"])
app.include_router(explain.router, prefix="/explain", tags=["explain"])
app.include_router(evaluate.router, prefix="/evaluate", tags=["evaluate"])
app.include_router(correct.router, prefix="/correct", tags=["correct"])


@app.get("/health")
async def health():
    return {"status": "ok"}
