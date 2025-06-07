from PIL import Image, ImageChops

from inky.auto import auto
from pdf2image import convert_from_path

from . import behaviour


def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)

class ShowOnInkyDisplayPrinter(behaviour.SaveFilePrinter):
    def run_after_saving(self, filename, ipp_request):
        images = convert_from_path(filename)
        im = images[0]
        im = trim(im)

        width, height = im.size

        if height > width:
            im = im.transpose(Image.Transpose.ROTATE_270)

        inky = auto(ask_user=True, verbose=True)

        canvas = Image.new("RGB", inky.resolution, inky.BLACK)

        im.thumbnail(inky.resolution)

        dw, dh = tuple(map(lambda i, j: i - j, inky.resolution, im.size))

        canvas.paste(im, (dw//2, dh//2))
        inky.set_image(canvas, saturation=0.5)
        inky.show()


