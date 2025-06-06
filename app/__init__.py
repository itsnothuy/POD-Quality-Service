from fastapi import FastAPI
from .api import v1, upload, health
from .storage import minio

def create_app() -> FastAPI:
    app = FastAPI(title="IQAS", version="0.2.0")
    app.include_router(v1.router, prefix="/v1")
    app.include_router(upload.router)
    app.include_router(health.router)
    @app.on_event("startup")
    def _warm_up_external():
        minio.init_bucket_blocking()
    return app
