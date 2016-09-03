"""This module contains code that actually generates the gradient image"""
# TODO this module is the first in the queue for massive refactoring

import math
from PIL import Image, ImageFilter
import random

Y = 1080
X = 1080
im = Image.new('RGBA', (X, Y))
ld = im.load()

STAGES = [0, 0.2, 0.5, 0.8, 1.]  # gradient stages


class Gradient(object):

    def __init__(self, mode='RGBA', x=1080, y=1080, rgb1=None, rgb2=None, stages=STAGES):
        self.img = Image.new(mode, (x, y))
        self.img_load = self.img.load()
        self.rgb1 = rgb1 if rgb1 else self.randcol()
        self.rgb2 = rgb2 if rgb2 else self.randcol()
        self.stages = stages
        self._generate()

    def _generate(self):
        rrng = self._get_rng(self.rgb1[0], self.rgb2[0], len(self.stages))
        grng = self._get_rng(self.rgb1[1], self.rgb2[1], len(self.stages))
        brng = self._get_rng(self.rgb1[2], self.rgb2[2], len(self.stages))
        heatmap = [[s, (rrng[i], grng[i], brng[i])] for i, s in enumerate(self.stages)]

        for y in range(self.img.size[1]):
            r, g, b = self.pixel(y, width=Y, map=heatmap)
            r, g, b = [int(256 * v) for v in (r, g, b)]
            for x in range(im.size[0]):
                self.img_load[x, y] = r, g, b

        self.img = self.img.filter(ImageFilter.SMOOTH_MORE)
        # applying some noise to get rid of banding
        self.img = Image.blend(self.img, self.get_white_noise_image(X, Y), alpha=0.03)

    def pixel(self, x, width=100, map=None, spread=1):
        width = float(width)
        map = map if map else []
        r = sum([self.gaussian(x, p[1][0], p[0] * width, width / (spread * len(map))) for p in map])
        g = sum([self.gaussian(x, p[1][1], p[0] * width, width / (spread * len(map))) for p in map])
        b = sum([self.gaussian(x, p[1][2], p[0] * width, width / (spread * len(map))) for p in map])
        return min(1.0, r), min(1.0, g), min(1.0, b)

    @staticmethod
    def randcol():
        return [float(random.randint(1, 5)) / 10 for x in range(3)]

    @staticmethod
    def _get_rng(a, b, sn=7):
        # I know. I know.
        sn = sn - 1
        rng = []
        for s in range(sn):
            rng.append(a + ((b - a) / sn) * (s))
        rng.append(b)
        return rng

    @staticmethod
    def gaussian(x, a, b, c, d=0):
        return a * math.exp(-(x - b) ** 2 / (2 * c ** 2)) + d

    @staticmethod
    def get_white_noise_image(width, height):
        pil_map = Image.new("RGBA", (width, height))
        random_grid = map(lambda x: (
                int(random.random() * 256),
                int(random.random() * 256),
                int(random.random() * 256)
            ), [0] * width * height)
        pil_map.putdata(random_grid)
        return pil_map

    def save(self, path):
        self.img.save(path, 'JPEG', subsampling=0, quality=95, optimize=True)


if __name__ == '__main__':
    gr = Gradient()
    gr.save("/home/wswld/Code/gradient_daily/temp.jpg")
