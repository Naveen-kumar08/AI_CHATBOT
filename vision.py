import base64


def encode_image(image_path):

    with open(image_path, "rb") as image:

        encoded = base64.b64encode(
            image.read()
        ).decode("utf-8")

    return encoded