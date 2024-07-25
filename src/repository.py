from typing import List

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError

from src.database import async_session_maker
from src.models import TaskORM
from src.schemas import TaskDB, TaskInput


class TaskRepository:
    @classmethod
    async def save_single_item_to_db(cls, item: TaskInput) -> TaskDB:
        async with async_session_maker() as session:
            async with session.begin():
                try:
                    data_dict = item.model_dump()
                    orm_obj = TaskORM(**data_dict)
                    session.add(orm_obj)
                    await session.commit()
                    return TaskDB.model_validate(orm_obj)
                except IntegrityError:
                    await session.rollback()
                    raise

    @classmethod
    async def get_items_list_from_db(cls) -> List[TaskDB]:
        async with async_session_maker() as session:
            async with session.begin():
                try:
                    result = await session.execute(select(TaskORM).order_by(TaskORM.id))
                    tasks = result.scalars().all()
                    return [TaskDB.model_validate(task) for task in tasks]
                except IntegrityError:
                    await session.rollback()
                    raise

    @classmethod
    async def get_item_by_id_from_db(cls, item_id: int) -> TaskDB | None:
        async with async_session_maker() as session:
            async with session.begin():
                try:
                    orm_obj = await session.get(TaskORM, item_id)
                    if orm_obj is None:
                        return None
                    return TaskDB.model_validate(orm_obj)
                except IntegrityError:
                    await session.rollback()
                    raise

    @classmethod
    async def delete_item_by_id_from_db(cls, item_id: int) -> bool:
        async with async_session_maker() as session:
            async with session.begin():
                try:
                    orm_obj = await session.get(TaskORM, item_id)
                    if orm_obj:
                        await session.delete(orm_obj)
                        await session.commit()
                        return True
                    return False
                except IntegrityError:
                    await session.rollback()
                    raise

    @classmethod
    async def update_item_in_db(
        cls, item_id: int, item_data: TaskInput
    ) -> TaskDB | None:
        async with async_session_maker() as session:
            async with session.begin():
                try:
                    result = await session.execute(
                        update(TaskORM)
                        .where(TaskORM.id == item_id)
                        .values(**item_data.model_dump())
                        .returning(TaskORM)
                    )
                    orm_obj = result.scalar_one_or_none()
                    if orm_obj is None:
                        return None
                    await session.commit()
                    return TaskDB.model_validate(orm_obj)
                except IntegrityError:
                    await session.rollback()
                    raise
