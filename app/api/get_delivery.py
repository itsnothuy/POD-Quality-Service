# from fastapi import APIRouter, HTTPException, Depends
# from sqlalchemy.future import select
# from sqlalchemy.ext.asyncio import AsyncSession
# from app.db.session import engine
# from app.db.models import Delivery

# router = APIRouter()

# @router.get("/{delivery_id}")
# async def get_delivery(delivery_id: str):
#     """
#     Look up a Delivery by ID and return its stored fields.
#     """
#     async with AsyncSession(engine) as session:
#         result = await session.execute(select(Delivery).where(Delivery.id == delivery_id))
#         record = result.scalars().first()
#         if not record:
#             raise HTTPException(status_code=404, detail="Not found")
#         return record

# app/api/get_delivery.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.db.models import Delivery
from sqlalchemy.future import select

router = APIRouter()

@router.get("/deliveries/{delivery_id}")
async def get_delivery(
    delivery_id: str,
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(
        select(Delivery).where(Delivery.id == delivery_id)
    )
    record = result.scalars().first()
    if record is None:
        raise HTTPException(status_code=404, detail="Not found")
    return record

