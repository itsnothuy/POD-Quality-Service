import cv2, numpy as np

def load_gray(bytestr: bytes):
    arr = np.frombuffer(bytestr, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError("Invalid image")
    return img
