from contextlib import asynccontextmanager


from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.util import await_fallback

from schemas import TaskAdd, TaskComplete
from models import init_db
import requests as rq


@asynccontextmanager
async def lifespan(app_: FastAPI):
    await init_db()
    print("Bot is ready")
    yield


app = FastAPI(title="To Do App", lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/tasks/{tg_id}")
async def tasks(tg_id: int):
    user = await rq.get_or_create_user(tg_id=tg_id)
    tasks = await rq.get_tasks(user_id=user.id)
    return tasks


@app.get("/api/main/{tg_id}")
async def profile(tg_id :int):
    user = await rq.get_or_create_user(tg_id=tg_id)
    completed_tasks_count = await rq.get_completed_tasks_count(user.id)
    return {"completedTasks": completed_tasks_count}


@app.post("/api/add")
async def add_task(task: TaskAdd):
    user = await rq.get_or_create_user(task.tg_id)
    await rq.add_task(user.id, task.title)
    return {"status": "ok"}


@app.patch("/api/completed")
async def complete_task(task: TaskComplete):
    await rq.complete_task(task.id)
    return {"status": "ok"}



