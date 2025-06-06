from fastapi import APIRouter, HTTPException
from app.storage import minio
router = APIRouter()

@router.get("/healthz", tags=["infra"])
def liveness():
    """
    Simple liveness check: attempt to list MinIO buckets.
    If it fails, return 503. Otherwise return { "ok": True }.
    """
    try:
        minio._s3.list_buckets()
    except Exception as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    return {"ok": True}
