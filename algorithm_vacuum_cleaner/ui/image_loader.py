import base64
import io

from PIL import Image, ImageTk


def load_image_from_b64(data):
    image_data = base64.b64decode(data)
    image = Image.open(io.BytesIO(image_data))
    return ImageTk.PhotoImage(image)