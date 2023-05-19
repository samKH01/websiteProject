import qrcode
from PIL import Image
from pyzbar.pyzbar import decode

def generate_qr_code(data, qr_size=(200, 200)):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img = img.resize(qr_size, Image.ANTIALIAS)
    return img

def decode_qr_code(image):
    decoded_data = decode(image)
    if decoded_data:
        return decoded_data[0].data.decode()
    return None
