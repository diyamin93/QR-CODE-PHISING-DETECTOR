import cv2
from pyzbar.pyzbar import decode


class QRDecoder:

    @staticmethod
    def decode_qr(image_path):

        image = cv2.imread(image_path)

        if image is None:
            return None

        decoded_objects = decode(image)

        for obj in decoded_objects:
            return obj.data.decode('utf-8')

        return None