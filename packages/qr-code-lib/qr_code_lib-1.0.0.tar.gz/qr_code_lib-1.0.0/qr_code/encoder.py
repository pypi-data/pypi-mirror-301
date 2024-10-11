import qrcode
from PIL import Image


def generate_qr_code(data: str, image_format: str = 'PNG') -> Image:
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    if image_format not in ['PNG', 'JPG', 'JPEG']:
        raise ValueError('Unsupported image format')
    return img
