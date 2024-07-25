from datetime import datetime

from pydantic import BaseModel, ConfigDict

from src.models import TaskStatus


class TaskInput(BaseModel):
    title: str
    description: str
    status: TaskStatus


class TaskDB(BaseModel):
    id: int
    title: str
    description: str
    status: TaskStatus
    created_at: datetime
    updated_at: datetime

    model_config: ConfigDict = ConfigDict(from_attributes=True)


class TaskOutput(TaskDB):
    pass
