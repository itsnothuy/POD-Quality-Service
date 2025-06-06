import cv2
from ..utils import imaging
from ..core.config import get_settings



def analyse(bytestr: bytes) -> dict:
    """
    Compute blur‐variance and mean‐intensity on a grayscale image.
    Returns a dict:
      {
        "blurry":   bool, 
        "underlit": bool,
        "blur_var": float,
        "mean":     float
      }
    Thresholds come from Settings.
    """
    gray = imaging.load_gray(bytestr)
    s = get_settings()
    blur_score  = cv2.Laplacian(gray, cv2.CV_64F).var()
    light_mean  = float(gray.mean())
    return {
        "blurry":   bool(blur_score < s.blur_thr),
        "underlit": bool(light_mean < s.light_thr),
        "blur_var": blur_score,
        "mean":     light_mean,
    }
