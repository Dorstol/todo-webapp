from types import new_class
from sqlalchemy import select, update, delete, func
from models import async_session, User, Task
from pydantic import BaseModel, ConfigDict
from typing import List
from schemas import TaskSchema


async def get_or_create_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            return user

        new_user = User(tg_id=tg_id)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user


async def get_tasks(user_id):
    async with async_session() as session:
        tasks = await session.scalars(
            select(Task).where(Task.user == user_id, Task.completed == False)
        )

        serialized_tasks = [TaskSchema.model_validate(t).model_dump() for t in tasks]

        return serialized_tasks


async def get_completed_tasks_count(user_id):
    async with async_session() as session:
        return await session.scalars(select(func.count(Task.id)).where(Task.completed == True))


async def add_task(user_id, title):
    async with async_session() as session:
        new_task = Task(
                title=title,
                user=user_id,
        )
        session.add(new_task)
        await session.commit()


async def complete_task(task_id):
    async with async_session() as session:
        await session.execute(update(Task).where(Task.id == task_id).value(completed=True))
        await session.commit()
