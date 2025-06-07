# app/api/v1.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.quality import analyse
from app.core.config import get_settings
from typing import Optional

router = APIRouter()

@router.post("/deliveries/v1/validate")
async def validate(
    image: UploadFile = File(...),
    blur_thr: Optional[int] = None,
    light_thr: Optional[int] = None,
):
    raw = await image.read()
    if not raw:
        raise HTTPException(status_code=400, detail="Empty upload")

    # allow per-request overrides
    if blur_thr is not None or light_thr is not None:
        s = get_settings()
        if blur_thr  is not None:
            s.blur_thr  = blur_thr
        if light_thr is not None:
            s.light_thr = light_thr

    try:
        result = analyse(raw)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    result["filename"] = image.filename
    return result
