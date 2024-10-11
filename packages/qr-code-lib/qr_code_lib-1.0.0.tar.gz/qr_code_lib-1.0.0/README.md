# QR Code Library

A Python library to encode and decode QR codes. 

## Features
- Encode a URL into a QR code image (supports PNG and JPG formats).
- Decode the content of a QR code image.

## Installation

```sh
pip install qr_code_lib
```

## Usage 

```bash
from qr_code_lib.encoder import generate_qr_code
from qr_code_lib.decoder import decode_qr_code

# Encode a URL into a QR code
img = generate_qr_code('https://www.example.com', image_format='PNG')
img.save('qrcode.png')

# Decode a QR code image
data = decode_qr_code('qrcode.png')
print(data)  # Output: https://www.example.com
```
