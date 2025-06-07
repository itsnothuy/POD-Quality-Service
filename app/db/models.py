from typing    import Optional
from uuid      import uuid4
from datetime  import datetime
from sqlmodel  import SQLModel, Field

class Delivery(SQLModel, table=True):
    """
    A Delivery record holds:
      - id:        a UUID4 string (primary key)
      - created_at:timestamp when the row was created
      - img_url:   the MinIO/S3 URL of the uploaded image
      - blurry:    bool flag from quality.analyse()
      - underlit:  bool flag from quality.analyse()
      - blur_var:  raw variance-of-Laplacian score (float)
      - mean:      raw mean intensity (float)
    """
    id:           str     = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    created_at:   datetime = Field(default_factory=datetime.utcnow, nullable=False)
    img_url:      str      = Field(nullable=False, index=True)
    blurry:       bool     = Field(nullable=False)
    underlit:     bool     = Field(nullable=False)
    blur_var:     float    = Field(nullable=False)
    mean:         float    = Field(nullable=False)
