from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException
from app.services import quality
from app.storage import minio
from app.db.session import engine
from app.db.models  import Delivery
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession 
import anyio

router = APIRouter()

def _process_and_store(data: bytes, delivery_id: str):
    """
    Background task: 
    1. Run the same quality.analyse() (so we can see flags + URL). 
    2. Upload the bytes to MinIO (getting a public URL).
    3. Print to stdout for now (in Phase 2 we'll persist to Postgres).
    If any error occurs (e.g. MinIO not reachable), swallow it.
    """
    try:
        flags = quality.analyse(data)
        url = minio.upload_bytes(data)
        # Persist to Postgres
        async def _save():
            async with AsyncSession(engine) as session:
                record = Delivery(
                    id=delivery_id,
                    img_url=url,
                    blurry=flags["blurry"],
                    underlit=flags["underlit"],
                    blur_var=flags["blur_var"],
                    mean=flags["mean"],
                )
                session.add(record)
                await session.commit()

        anyio.run(_save)
        print(f"[{delivery_id}] stored → {url} flags: {flags}")
        return flags | {"img_url": url}
    except Exception:
        return

@router.post("/deliveries/{delivery_id}/photo")
async def upload_photo(
        delivery_id: str,
        bg: BackgroundTasks,
        image: UploadFile = File(...)
):
    """
    1. Read the raw bytes from `image`.
    2. If empty → 400.
    3. Kick off background task to upload + analyse again.
    4. Return { delivery_id, blurry, underlit, blur_var, mean } immediately.
    """
    data = await image.read()
    if not data:
        raise HTTPException(status_code=400, detail="Empty upload")
    
    # First pass: get the flags synchronously
    flags = quality.analyse(data)
    # Then schedule the background task (re-analysis + actual MinIO upload)
    bg.add_task(_process_and_store, data, delivery_id)
    return {"delivery_id": delivery_id, **flags}
