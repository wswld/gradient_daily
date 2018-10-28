"""This module contains code that actually generates the gradient image"""
# TODO this module is the first in the queue for massive refactoring

from colour import Color
from PIL import Image, ImageFilter
import random

Y = 1080
X = 1080


class Gradient(object):

    def __init__(self, mode='RGBA', x=X, y=Y, rgb1=None, rgb2=None):
        self.img = Image.new(mode, (x, y))
        self.img_load = self.img.load()
        randfloat = lambda: "%.2f" % random.random()
        randcol = lambda: (randfloat(), randfloat(), randfloat())
        c1 = Color(rgb=rgb1) if rgb1 else Color(rgb=randcol())
        c2 = Color(rgb=rgb2) if rgb2 else Color(rgb=randcol())
        ysize = self.img.size[1]
        colrange = list(c1.range_to(c2, ysize))
        for y in range(ysize):
            r, g, b = [int(256 * v) for v in (colrange[y].red, colrange[y].green, colrange[y].blue)]
            for x in range(self.img.size[0]):
                self.img_load[x, y] = r, g, b
        self.img = self.img.filter(ImageFilter.SMOOTH_MORE)
        # applying some noise to get rid of banding
        self.img = Image.blend(self.img, self.get_white_noise_image(X, Y), alpha=0.03)

    @staticmethod
    def get_white_noise_image(width, height):
        pil_map = Image.new("RGBA", (width, height))
        random_grid = map(lambda x: (
            int(random.random() * 256),
            int(random.random() * 256),
            int(random.random() * 256)
        ), [0] * width * height)
        pil_map.putdata(list(random_grid))
        return pil_map

    def save(self, path):
        self.img.save(path, 'JPEG', subsampling=0, quality=95, optimize=True)
        self.img.close()

if __name__ == '__main__':
    gr = Gradient()
    gr.save("/tmp/temp.jpg")
