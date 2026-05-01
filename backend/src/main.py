from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.database import init_pool, close_pool
from src.api.routes import students, explain, evaluate, correct


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.pool = await init_pool()
    yield
    await close_pool(app.state.pool)


app = FastAPI(lifespan=lifespan)

app.include_router(students.router, prefix="/students", tags=["students"])
app.include_router(explain.router, prefix="/explain", tags=["explain"])
app.include_router(evaluate.router, prefix="/evaluate", tags=["evaluate"])
app.include_router(correct.router, prefix="/correct", tags=["correct"])


@app.get("/health")
async def health():
    return {"status": "ok"}
