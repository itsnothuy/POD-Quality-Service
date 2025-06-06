from fastapi import APIRouter, UploadFile, File, HTTPException
from ..services import quality
from ..core.config import get_settings

router = APIRouter()

@router.post("/validate")
async def validate(
    image: UploadFile = File(...),
    blur_thr:  int | None = None,
    light_thr:  int | None = None,
):
    """
    1. Optionally override blur_thr / light_thr via query params. 
    2. Run quality.analyse() on the raw bytes.
    3. Return the JSON containing { blurry, underlit, blur_var, mean }.
    """
    raw = await image.read()
    if not raw:
        raise HTTPException(status_code=400, detail="Empty upload")

    # If the user passed new thresholds, override them in Settings (process‐wide).
    if blur_thr is not None or light_thr is not None:
        s = get_settings()
        if blur_thr  is not None:
            s.blur_thr  = blur_thr
        if light_thr is not None:
            s.light_thr = light_thr

    try:
        result = quality.analyse(raw)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    result["filename"] = image.filename
    return result
