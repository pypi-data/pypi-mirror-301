import cv2
from PIL import Image
import numpy as np


def decode_qr_code(image_path: str) -> str:
    img = cv2.imread(image_path)
    detector = cv2.QRCodeDetector()
    data, vertices_array, binary_qrcode = detector.detectAndDecode(img)
    if vertices_array is not None:
        return data
    else:
        raise ValueError("QR code not detected")
