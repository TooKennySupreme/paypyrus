__author__ = 'Manikandan'

from qrcode import *

qr = QRCode(
    version=4,
    error_correction= ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data('Test code for the paypyrus hack')
qr.make(fit=True)

img = qr.make_image()
img.save("test-py.png")
