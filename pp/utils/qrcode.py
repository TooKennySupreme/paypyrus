import pyqrcode, svgwrite
import sys, os
from .. import models
from .. import config
from io import BytesIO
import random, string

def get_str():
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))

def create_redemption_url(bill_token):
    return "{}/redeem/{}".format(config.current_host, bill_token)

def qrfilegen(token, creator):
    qrfilename = get_str()
    link = create_redemption_url(token)

    url = pyqrcode.QRCode(link)
    handle = BytesIO()
    url.svg(handle, scale = 1, xmldecl=False)
    tup = handle.getvalue().decode("UTF-8")
    string_svg = "".join(tup)
    b64_svg = string_svg.encode("base64")
    # Saves a b64 representation of the SVG in the QRCode db model
    save_qr(token, b64_svg, creator)

def save_qr(token, svg_string, creator="noone"):
    sq = models.QRCode.select().where(models.QRCode.qr_token == token)
    if not sq.exists():
        models.QRCode.create(
            qr_token = token,
            qr_code_string = svg_string,
            creator = creator
        )

def create_svg(token):
    # function obseleted by show_bill.html Jinja template
    svg_document = svgwrite.Drawing(filename = "qrcodegen.svg", size = ("400px", "300px"))
    svg_document.add(svg_document.image("paysign1.svg", insert = (0,0), size = ("35px", "35px")))
    svg_document.add(svg_document.image("paysign1.svg", insert = (0,200), size = ("35px", "35px")))
    svg_document.add(svg_document.image("paysign1.svg", insert = (300,0), size = ("35px", "35px")))
    svg_document.add(svg_document.image("paysign1.svg", insert = (300,200), size = ("35px", "35px")))
    svg_document.add(svg_document.image("paypyrus-sign.svg", insert = (55,5), size = ("300px", "300px")))

    qrstr = qrfilegen(token)

    svg_document.add(svg_document.image(qrstr, insert=(80, 40), size=("175px", "175px")))
    string = svg_document.tostring()
    return string
