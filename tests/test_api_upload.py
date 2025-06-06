from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_upload_ok(tmp_path):
    """
    1. Create a 50×50 white JPEG (using OpenCV).
    2. POST it to /deliveries/abc123/photo.
    3. Expect 200 and JSON containing blur/underlit keys.
    """
    import cv2
    import numpy as np

    img = tmp_path / "white.jpg"
    cv2.imwrite(str(img), np.ones((50,50,3), np.uint8) * 255)

    with img.open("rb") as f:
        response = client.post(
            "/deliveries/abc123/photo",
            files={"image": ("white.jpg", f, "image/jpeg")}
        )

    assert response.status_code == 200
    body = response.json()
    assert "blurry" in body and "underlit" in body
    assert body["delivery_id"] == "abc123"
