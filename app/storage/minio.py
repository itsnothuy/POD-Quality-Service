import io
import uuid
import boto3
from botocore.client import Config
from tenacity import retry, stop_after_attempt, wait_fixed
import botocore.exceptions
from ..core.config import get_settings



# _MINIO_ENDPOINT = "http://minio:9000"          # container name!
# _BUCKET         = os.getenv("MINIO_BUCKET", "pod-images")


s = get_settings()
# Create a boto3 S3‐compatible client pointing at MinIO
_s3 = boto3.session.Session().client(
    service_name="s3",
    aws_access_key_id=s.minio_root_user,
    aws_secret_access_key=s.minio_root_password,
    endpoint_url=s.minio_endpoint_internal,
    config=Config(signature_version="s3v4"),
)
def init_bucket() -> None:
    """
    Create the bucket if it doesn't exist. Raises on real errors.
    """
    existing = [b["Name"] for b in _s3.list_buckets().get("Buckets", [])]
    if s.minio_bucket not in existing:
        _s3.create_bucket(Bucket=s.minio_bucket)

@retry(stop=stop_after_attempt(10), wait=wait_fixed(1))
def _wait_conn() -> None:
    """
    Poll MinIO until it responds. Retries up to 10 times with 1s intervals.
    """
    _s3.list_buckets()

def init_bucket_blocking() -> None:
    """
    Retry‐safe “ensure that the bucket exists” (invoked on startup).
    """
    _wait_conn()
    init_bucket()

def upload_bytes(data: bytes, suffix: str = ".jpg") -> str:
    """
    Upload the raw bytes into MinIO and return a PUBLIC URL.
    - Uses a random UUID4 + suffix as the key.
    - Sets ACL="public-read" for simplicity (dev mode).
    """
    key = f"{uuid.uuid4()}{suffix}"
    _s3.put_object(
        Bucket=s.minio_bucket,
        Key=key,
        Body=io.BytesIO(data),
        ACL="public-read"
    )
    # Return the public‐facing path (localhost version)
    return f"{s.minio_public_endpoint}/{s.minio_bucket}/{key}"
