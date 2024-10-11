import unittest
from qr_code.encoder import generate_qr_code
from qr_code.decoder import decode_qr_code


class TestQRCodeLib(unittest.TestCase):

    def test_generate_and_decode_qr_code(self):
        data = "https://www.example.com"
        img = generate_qr_code(data, image_format='PNG')
        img_path = 'test_qr.png'
        img.save(img_path)
        decoded_data = decode_qr_code(img_path)
        self.assertEqual(data, decoded_data)


if __name__ == '__main__':
    unittest.main()
