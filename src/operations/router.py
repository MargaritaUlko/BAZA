import time
from datetime import timezone

from fastapi import APIRouter, HTTPException, FastAPI
from fastapi import Depends
from fastapi_cache.decorator import cache
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from database import get_async_session
from .models import operation
from .schemas import OperationCreate

router = APIRouter(
    prefix = "/operations",
    tags=["operation"],

)
import logging

logger = logging.getLogger(__name__)





@router.get("/", response_model=list[OperationCreate])
async def get_operations(operation_type: str, session: AsyncSession = Depends(get_async_session)):
    try:
        logger.debug(f"Received operation_type: {operation_type}")
        query = select(operation).where(operation.c.type == operation_type)
        logger.debug(f"Executing query: {query}")
        result = await session.execute(query)
        operations = result.fetchall()  # Fetch all rows
        logger.debug(f"Fetched operations: {operations}")

        # Convert ORM objects to Pydantic models
        operation_list = [OperationCreate.from_orm(row) for row in operations]

        # Log if no operations were found
        if not operation_list:
            logger.warning(f"No operations found for type: {operation_type}")

        return operation_list
    except Exception as e:
        logger.error(f"Failed to fetch operations: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch operations: {str(e)}")



@router.post("/")
async def create_operation(new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        # Проверяем, что new_operation.date содержит информацию о часовом поясе
        if new_operation.date.tzinfo:
            # Приводим к UTC, если объект offset-aware
            utc_date = new_operation.date.astimezone(timezone.utc).replace(tzinfo=None)
        else:
            # Или используем как есть, если объект offset-naive
            utc_date = new_operation.date

        await session.execute(
            operation.insert().values(
                id=new_operation.id,
                quantity=new_operation.quantity,
                figi=new_operation.figi,
                type=new_operation.type,
                date=utc_date,
            )
        )
        await session.commit()
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create operation: {str(e)}")

@router.get("/bebra/")
@cache(expire = 60)
def long_operation():
    time.sleep(9)
    return {"ijkn":"bebra123"}
# ORM - Object relational-Model
# SQL Injection

