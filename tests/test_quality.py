"""
Minimal pytest suite for `app.services.quality.analyse`.

Creates synthetic images in-memory so the tests run anywhere—no fixture files
needed, no OpenCV GUI calls in CI.
"""
import cv2
import numpy as np
from app.services.quality import analyse

def _encode(img: np.ndarray) -> bytes:
    """Utility: encode BGR/gray ndarray → JPG bytes."""
    success, buf = cv2.imencode(".jpg", img)
    assert success, "cv2.imencode failed"
    return buf.tobytes()


def test_blurry_flag_true():
    """
    Make a totally blurred image by applying a heavy Gaussian blur.
    Expect analyse(... )['blurry'] to be True.
    """
    sharp = np.zeros((100, 100), np.uint8) + 255        # white square
    blurry = cv2.GaussianBlur(sharp, (31, 31), 0)
    result = analyse(_encode(blurry))
    assert result["blurry"] is True, result


def test_blurry_flag_false():
    """
    Draw crisp text on a solid background → should NOT be blurry.
    """
    img = np.zeros((100, 300), np.uint8) + 255          # white strip
    cv2.putText(img, "ABCDE", (5, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 2, 0, 3, cv2.LINE_AA)
    result = analyse(_encode(img))
    assert result["blurry"] is False, result


def test_underlit_true():
    """
    All-black image → mean intensity ≈ 0 → 'underlit' must be True.
    """
    dark = np.zeros((100, 100), np.uint8)
    result = analyse(_encode(dark))
    assert result["underlit"] is True, result


def test_underlit_false():
    """
    Bright image → mean intensity high → 'underlit' must be False.
    """
    bright = np.ones((100, 100), np.uint8) * 255
    result = analyse(_encode(bright))
    assert result["underlit"] is False, result
