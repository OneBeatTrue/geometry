from PIL import Image
import numpy as np
from affine import Affine

size_x, size_y = 100, 100
img = Image.new("RGB", (size_x, size_y), "white")
pixels = img.load()
affine = Affine()


def draw(arr):
    for dot in arr:
        x, y = dot[0], dot[1]
        pixels[max(0, min(size_x - 1, x + size_x // 2)), max(0, min(size_y - 1, size_y - y - 1 - size_y // 2))] = (0, 0, 0)


def draw_axis():
    for x in range(size_x):
        pixels[x, size_y // 2] = (128, 128, 128)
        if x == size_x // 2:
            for y in range(size_y):
                pixels[x, y] = (128, 128, 128)


def extend_round(arr):
    arr.extend(affine.Sxy(arr))
    arr.extend(affine.Sx(arr))
    arr.extend(affine.Sy(arr))


def draw_simple_a(r):
    arr = []
    for x in range(0, int(np.ceil(r / np.sqrt(2)))):
        arr.append([x, np.round(np.sqrt(r ** 2 - x ** 2)), 1])
    extend_round(arr)
    draw(arr)


def draw_simple_b(R):
    arr = []
    for alpha in np.linspace(np.pi / 2, np.pi / 4, R):
        arr.append([int(np.round(R * np.cos(alpha))),
                    int(np.round(R * np.sin(alpha))),
                    1])
    extend_round(arr)
    draw(arr)


def draw_bresenham(r):
    x = 0
    y = r
    d = 3 - 2 * r
    arr = []
    while x <= y:
        arr.append([x, y, 1])
        if d >= 0:
            d = d + 4 * (x - y) + 10
            y -= 1
        else:
            d = d + 4 * x + 6
        x += 1
    extend_round(arr)
    # arr = affine.Ro(np.pi / 3, arr)
    draw(arr)


r = 10
draw_axis()
# draw_simple_a(r)
# draw_simple_b(r)
draw_bresenham(r)

img.show()
