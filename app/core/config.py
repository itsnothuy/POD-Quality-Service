from functools   import lru_cache
from pydantic    import BaseSettings

class Settings(BaseSettings):
    # IQAS thresholds
    blur_thr:  int = 100
    light_thr: int = 60

    # MinIO / S3
    minio_endpoint_internal: str = "http://minio:9000"
    minio_public_endpoint:   str = "http://localhost:9000"
    minio_root_user:         str = "minioadmin"
    minio_root_password:     str = "minioadmin"
    minio_bucket:            str = "pod-images"

    class Config:            # `.env` already in repo – keep using it
        env_file = ".env"

@lru_cache
def get_settings() -> Settings:          # cheap singleton accessor
    return Settings()
