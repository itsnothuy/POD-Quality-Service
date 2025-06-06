from fastapi import FastAPI
from .api import v1

def create_app() -> FastAPI:
    app = FastAPI(title="IQAS", version="0.2.0")
    app.include_router(v1.router, prefix="/v1")
    return app
