import pyqrcode
import svgwrite
import sys
import os

# from io import BytesIO
import random, string

def get_str():
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))


def qrfilegen(link):
    qrfilename = get_str()
    correct = False
    while correct != True:
        relative = "qr-{}.svg".format(qrfilename)
        gen_fn = "pp/static/svgs/{}".format(relative)
        if os.path.isfile(gen_fn):
            continue
        else:
            correct = True
    url = pyqrcode.QRCode(link)
    url.svg(gen_fn, scale=1, xmldecl=False)
    return relative
    #handle = BytesIO()
    #url = pyqrcode.QRCode(qrcodeval)
    #url.svg(handle, scale = 2, xmldecl=False)
    #tup = handle.getvalue().decode("UTF-8")
    #print("".join(tup))
    #return "".join(tup)
    #return handle

def svgfilename(link):
    svg_document = svgwrite.Drawing(filename = "qrcodegen.svg", size = ("400px", "400px"))
    svg_document.add(svg_document.image("paysign1.svg", insert = (0,0), size = ("35px", "35px")))
    svg_document.add(svg_document.image("paysign1.svg", insert = (0,200), size = ("35px", "35px")))
    svg_document.add(svg_document.image("paysign1.svg", insert = (300,0), size = ("35px", "35px")))
    svg_document.add(svg_document.image("paysign1.svg", insert = (300,200), size = ("35px", "35px")))
    svg_document.add(svg_document.image("paypyrus-sign.svg", insert = (55,5), size = ("300px", "300px")))
    qrstr = qrfilegen(link)
    svg_document.add(svg_document.image(qrstr, insert=(80, 40), size=("175px", "175px")))
    string = svg_document.tostring()
    correct = False
    while correct != True:
        qrfilename = get_str()
        relative = "final-{}.svg".format(qrfilename)
        fn = "pp/static/svgs/{}".format(relative)
        if os.path.isfile(fn):
            continue
        else:
            correct = True

    with open(fn, "w") as f:
        f.write(svg_document.tostring())

    return relative

if __name__ == "__main__":
    svgfilename("http://google.com")
