"""This module contains code that actually generates the gradient image"""
# TODO this module is the first in the queue for massive refactoring
import logging
from PIL import Image, ImageFilter
import random

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')

Y = 1080
X = 1080


class Gradient(object):

    def __init__(self, mode='RGBA', x=X, y=Y, rgb1=None, rgb2=None):
        self.img = Image.new(mode, (x, y))
        self.img_load = self.img.load()
        randfloat = lambda: float("%.2f" % random.random())
        self.rgb1 = (randfloat()*256, randfloat()*256, randfloat()*256,)
        self.rgb2 = (randfloat()*256, randfloat()*256, randfloat()*256,)
        logger.debug(f"Color I: {self.rgb1[0]} {self.rgb1[1]} {self.rgb1[2]}")
        logger.debug(f"Color II: {self.rgb2[0]} {self.rgb2[1]} {self.rgb2[2]}")
        self._populate_y_gradient()
        for y in range(self.img.size[1]):
            for x in range(self.img.size[0]):
                self.img_load[x, y] = self.y_gradient[y-1][0], self.y_gradient[y-1][1], self.y_gradient[y-1][2]
        self.img = self.img.filter(ImageFilter.SMOOTH_MORE)
        # applying some noise to get rid of banding
        self.img = Image.blend(self.img, self.get_white_noise_image(X, Y), alpha=0.03)

    def _populate_y_gradient(self):
        ysize = self.img.size[1]
        r_step = (self.rgb2[0] - self.rgb1[0])/ysize
        g_step = (self.rgb2[1] - self.rgb1[1])/ysize
        b_step = (self.rgb2[2] - self.rgb1[2])/ysize
        self.y_gradient = [(
            int(self.rgb1[0]+r_step*y),
            int(self.rgb1[1]+g_step*y),
            int(self.rgb1[2]+b_step*y)
            ) for y in range(ysize)]

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
        img = self.img.convert('RGB')
        img.save(path, format="JPEG", subsampling=0, quality=95, optimize=True)
        self.img.close()

if __name__ == '__main__':
    gr = Gradient()
    gr.save("/tmp/temp.jpg")
