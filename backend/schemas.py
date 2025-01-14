from pydantic import BaseModel, ConfigDict


class TaskSchema(BaseModel):
    id: int
    title: str
    completed: bool
    user: int

    model_config = ConfigDict(from_attributes=True)

class TaskAdd(BaseModel):
    tg_id: int
    title: str

class TaskComplete(BaseModel):
    id: int
