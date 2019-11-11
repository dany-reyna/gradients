import math

from PIL import Image
from pathlib import Path
import matplotlib.pyplot as plt

from colors import colors, WHITE
from helpers import random_filename

SIZE = 750


def gaussian(x, a, b, c, d=0):
    return a * math.exp(-(x - b) ** 2 / (2 * c ** 2)) + d


def pixel(x, map_, width=100, spread=0.7):
    width = float(width)
    r = sum([gaussian(x, p[1][0], p[0] * width, width / (spread * len(map_))) for p in map_])
    g = sum([gaussian(x, p[1][1], p[0] * width, width / (spread * len(map_))) for p in map_])
    b = sum([gaussian(x, p[1][2], p[0] * width, width / (spread * len(map_))) for p in map_])
    return min(1.0, r), min(1.0, g), min(1.0, b)


def linear(map_, im, ld):
    for x in range(im.size[0]):
        r, g, b = pixel(x, map_, width=SIZE)
        r, g, b = [int(256 * v) for v in (r, g, b)]
        for y in range(im.size[1]):
            ld[x, y] = r, g, b


def diagonal(map_, im, ld):
    for y in range(im.size[1]):
        r, g, b = pixel(y, map_, width=SIZE)
        r, g, b = [int(256 * v) for v in (r, g, b)]
        for x in range(y):
            ld[x, y - x] = r, g, b

    for y in range(im.size[1]):
        r, g, b = pixel((SIZE * 2 - 1) - y, map_, width=SIZE)
        r, g, b = [int(256 * v) for v in (r, g, b)]
        for x in range(y):
            ld[(SIZE - 1) - x, (SIZE - 1) - (y - x)] = r, g, b


def generate_linear(map_, im, ld, out_path):
    for _ in range(4):
        linear(map_, im, ld)
        im = im.rotate(90)
        im.save(random_filename(str(out_path), ".jpg"))


def generate_diagonal(map_, im, ld, out_path):
    for _ in range(4):
        diagonal(map_, im, ld)
        im = im.rotate(90)
        im.save(random_filename(str(out_path), ".jpg"))


if __name__ == '__main__':
    # A map_ of rgb points in your distribution
    # [distance, (r, g, b)]
    # distance is percentage from edge
    # heatmap = [
    #     [1.0, (0.15, 0.26, 0.48)],
    #     [-0.6, (1.0, 1.0, 1.0)],
    # ]

    out_path = Path.cwd() / 'data'

    image = Image.new('RGB', (SIZE, SIZE))
    pixel_data = image.load()

    maps = []
    maps.append((colors[87  ], WHITE))

    for m in maps:
        generate_linear(m, image, pixel_data, out_path)
        generate_diagonal(m, image, pixel_data, out_path)
