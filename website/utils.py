import os
from PIL import Image, ImageOps

ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}


def allowed_file(filename):
    """
    Check if the given file has an allowed extension.
    :param filename: The name of the file to check.
    :return: True if the file has an allowed extension, False otherwise.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def resize_image(image, max_size=(800, 800)):
    """
    Resize an image to fit within the specified dimensions while maintaining aspect ratio.
    :param image: The input PIL Image object.
    :param max_size: A tuple (width, height) representing the maximum dimensions of the resized image.
    :return: A new PIL Image object containing the resized image.
    """
    img = ImageOps.fit(image, max_size, Image.ANTIALIAS)
    return img


def add_qr_code_to_document(document, qr_code):
    """
    Add a QR code to the bottom of the document.
    :param document: The input document as a PIL Image object.
    :param qr_code: The QR code as a PIL Image object.
    :return: A new PIL Image object containing the document with the QR code added to the bottom.
    """
    # Calculate the size and position for the QR code
    qr_size = qr_code.size
    doc_width, doc_height = document.size
    qr_position = (doc_width - qr_size[0], doc_height)

    # Create a new image with additional space for the QR code
    new_height = doc_height + qr_size[1]
    new_image = Image.new('RGB', (doc_width, new_height), 'white')

    # Paste the document and QR code onto the new image
    new_image.paste(document, (0, 0))
    new_image.paste(qr_code, qr_position)

    return new_image

def save_uploaded_document():
    pass