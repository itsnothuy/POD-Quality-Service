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
    
    # Postgres
    postgres_host:     str = "postgres"
    postgres_port:     int = 5432
    postgres_db:       str = "iqas"
    postgres_user:     str = "iqas"
    postgres_password: str = "iqas_pass"

    class Config:            # `.env` already in repo – keep using it
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache
def get_settings() -> Settings:          # cheap singleton accessor
    return Settings()
