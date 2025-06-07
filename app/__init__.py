# app/__init__.py
from fastapi import FastAPI
from contextlib import asynccontextmanager

def create_app() -> FastAPI:
    # delayed imports so that dependencies are only loaded when the app is created
    from .api.health       import router as health_router
    from .api.upload       import router as upload_router
    from .api.get_delivery import router as get_delivery_router
    from .api.v1           import router as v1_router
    from .db.session       import init_db
    from .storage.minio    import init_bucket_blocking

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # → Startup logic
        await init_db()
        init_bucket_blocking()
        yield
        # → Shutdown logic (if you ever need it, e.g. closing DB connections)
        # await close_db()
        # cleanup_bucket()

    app = FastAPI(
        title="POD Screenshot Service",
        lifespan=lifespan
    )

    app.include_router(health_router)
    app.include_router(upload_router)
    app.include_router(get_delivery_router)
    app.include_router(v1_router)


    return app

app = create_app()
