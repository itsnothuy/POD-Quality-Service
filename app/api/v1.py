from fastapi import APIRouter, UploadFile, File, HTTPException
from ..services import quality

router = APIRouter()

@router.post("/validate")
async def validate(image: UploadFile = File(...)):
    try:
        result = quality.analyse(await image.read())
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    result["filename"] = image.filename
    return result
