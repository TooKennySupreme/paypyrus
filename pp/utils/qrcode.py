import pyqrcode
import svgwrite
import sys
from io import BytesIO
from io import FileIO
import random
import string
import asyncio
from threading import Thread
from io import BufferedIOBase
from pprint import pprint

def qrfilegen():
    qrfilename = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(100))
    url = pyqrcode.QRCode()
    #handle = BytesIO()
    #url = pyqrcode.QRCode(qrcodeval)
    #url.svg(handle, scale = 2, xmldecl=False)
    #tup = handle.getvalue().decode("UTF-8")
    #print("".join(tup))
    #return "".join(tup)
    #return handle

def svgfilename():
    fileio = FileIO('helllo')
    svg_document = svgwrite.Drawing(filename = "qrcodegen.svg",size = ("1000px", "1000px"))
    svg_document.add(svg_document.image("paysign1.svg", insert = (0,0), size = ("35px", "35px")))
    svg_document.add(svg_document.image("paysign1.svg", insert = (0,200), size = ("35px", "35px")))
    svg_document.add(svg_document.image("paysign1.svg", insert = (300,0), size = ("35px", "35px")))
    svg_document.add(svg_document.image("paysign1.svg", insert = (300,200), size = ("35px", "35px")))
    svg_document.add(svg_document.image("paypyrus-sign.svg", insert = (55,5), size = ("300px", "300px")))
    qrstr = qrfilegen("http:nonsesns")
    fileio.write(qrstr)
    svg_document.add(svg_document.image(fileio, insert=(80, 40), size=("250px", "250px")))
    print(svg_document.tostring())
    f = open('qrcodegenfinal.svg', 'w')
    f.write(svg_document.tostring())
    f.close()
    return svg_document.tostring()





