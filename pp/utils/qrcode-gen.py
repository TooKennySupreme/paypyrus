__author__ = 'Manikandan'

import qrcode
import qrcode.image.svg

qr = qrcode.QRCode(
    version=4,
    error_correction= qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data('Test code for the paypyrus hack')
qr.make(fit=True)

factory = qrcode.image.svg.SvgFragmentImage
img1 = qrcode.make("Blah blah blah", image_factory = factory)
img1.save("test-svg.svg")


img = qr.make_image()
img.save("test-py.png")
