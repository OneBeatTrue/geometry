from PIL import Image
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


def draw_simple(xa, ya, xb, yb):
    arr = []
    for x in range(xa, xb):
        arr.append([x, round((yb - ya) / (xb - xa) * (x - xa) + ya), 1])
    draw(arr)


def draw_bresenham(xa, ya, xb, yb):
    tan = (yb - ya) / (xb - xa)

    sx = tan < 0
    if sx:
        tan *= -1
        ya *= -1
        yb *= -1

    sxy = tan > 1
    if sxy:
        xa, ya = ya, xa
        xb, yb = yb, xb

    dx, dy = xb - xa, yb - ya
    y = 0
    d = 2 * dy - 2 * dx
    arr = []
    for x in range(0, dx, 1):
        arr.append([x, y, 1])
        if d >= 0:
            y += 1
        d = d + 2 * dy - 2 * (y - arr[-1][1]) * dx
    arr = affine.Ta([xa, ya], arr)

    if sxy:
        arr = affine.Sxy(arr)
        xa, ya = ya, xa
        xb, yb = yb, xb

    if sx:
        arr = affine.Sx(arr)
        ya *= -1
        yb *= -1

    draw(arr)


xa, ya = -10, -7
xb, yb = 15, 23
draw_axis()
# draw_simple(xa, ya, xb, yb)
draw_bresenham(xa, ya, xb, yb)

img.show()
