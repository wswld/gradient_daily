"""This module contains code that actually generates the gradient image"""
# TODO this module is the first in the queue for massive refactoring

import math
from PIL import Image, ImageFilter
import random

Y = 2024
X = 2024
im = Image.new('RGB', (X, Y))
ld = im.load()

stages = [0, 0.2, 0.5, 0.8, 1.]


def randcol():
    return [float(random.randint(1, 5)) / 10 for x in range(3)]


rgb1 = randcol()
rgb2 = randcol()


def get_rng(a, b, sn=7):
    # I know. I know.
    sn = sn - 1
    rng = []
    for s in range(sn):
        rng.append(a + ((b - a) / sn) * (s))
    rng.append(b)
    return rng


rrng = get_rng(rgb1[0], rgb2[0], len(stages))
grng = get_rng(rgb1[1], rgb2[1], len(stages))
brng = get_rng(rgb1[2], rgb2[2], len(stages))

heatmap = [[s, (rrng[i], grng[i], brng[i])] for i, s in enumerate(stages)]


def gaussian(x, a, b, c, d=0):
    return a * math.exp(-(x - b) ** 2 / (2 * c ** 2)) + d


def pixel(x, width=100, map=[], spread=1):
    width = float(width)
    r = sum([gaussian(x, p[1][0], p[0] * width, width / (spread * len(map))) for p in map])
    g = sum([gaussian(x, p[1][1], p[0] * width, width / (spread * len(map))) for p in map])
    b = sum([gaussian(x, p[1][2], p[0] * width, width / (spread * len(map))) for p in map])
    return min(1.0, r), min(1.0, g), min(1.0, b)


for y in range(im.size[1]):
    r, g, b = pixel(y, width=Y, map=heatmap)
    r, g, b = [int(256 * v) for v in (r, g, b)]
    for x in range(im.size[0]):
        ld[x, y] = r, g, b


def produce():
    global im
    for r in range(10):
        # TODO: doesn't seem to smooth the image up
        im.filter(ImageFilter.BLUR)
    return im
