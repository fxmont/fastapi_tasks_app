from typing import Annotated, List

from fastapi import APIRouter, Body, HTTPException, Path, Response, status

from src.repository import TaskRepository
from src.schemas import TaskDB, TaskInput, TaskOutput

router = APIRouter(
    prefix="/tasks",
    tags=["Задачи"],
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TaskOutput)
async def create_task(task: TaskInput) -> TaskDB:
    task_db = await TaskRepository.save_single_item_to_db(task)
    return task_db


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[TaskOutput])
async def get_tasks() -> List[TaskDB]:
    tasks = await TaskRepository.get_items_list_from_db()
    return tasks


@router.get("/{task_id}", status_code=status.HTTP_200_OK, response_model=TaskOutput)
async def get_single_task(task_id: Annotated[int, Path(ge=1)]) -> TaskDB:
    task = await TaskRepository.get_item_by_id_from_db(task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return task


@router.put("/{task_id}", status_code=status.HTTP_200_OK, response_model=TaskOutput)
async def update_single_task(
    task_id: Annotated[int, Path(ge=1)], task_data: Annotated[TaskInput, Body()]
):
    task = await TaskRepository.update_item_in_db(task_id, task_data)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_single_task(task_id: Annotated[int, Path(ge=1)]):
    deleted = await TaskRepository.delete_item_by_id_from_db(task_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
