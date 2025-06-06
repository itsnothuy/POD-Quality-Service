import cv2
from . import imaging

BLUR_THR  = 100
LIGHT_THR = 60

def analyse(bytestr: bytes) -> dict:
    gray = imaging.load_gray(bytestr)
    blur_score  = cv2.Laplacian(gray, cv2.CV_64F).var()
    light_mean  = gray.mean()
    return {
        "blurry":   blur_score < BLUR_THR,
        "underlit": light_mean < LIGHT_THR,
        "blur_var": blur_score,
        "mean":     light_mean,
    }
