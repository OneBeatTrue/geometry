from PIL import Image
from affine import Affine
import numpy as np

size_x, size_y = 1000, 1000
img = Image.new("RGB", (size_x, size_y), "white")
pixels = img.load()
affine = Affine()
t_arr = np.linspace(0, 1, 10000)


def draw(arr, color=(0, 0, 0)):
    for dot in arr:
        x, y = dot[0], dot[1]
        pixels[max(0, min(size_x - 1, x + size_x // 2)), max(0, min(size_y - 1, size_y - y - 1 - size_y // 2))] = color


def draw_axis():
    for x in range(size_x):
        pixels[x, size_y // 2] = (128, 128, 128)
        if x == size_x // 2:
            for y in range(size_y):
                pixels[x, y] = (128, 128, 128)


def get_bezier_curve_2(arr):
    p_0, p_1, p_2 = arr
    return [np.round((1 - t) ** 2 * p_0 + 2 * (1 - t) * t * p_1 + t ** 2 * p_2) for t in t_arr]


def get_bezier_curve_3(arr):
    p_0, p_1, p_2, p_3 = arr
    return [np.round((1 - t) ** 3 * p_0 + 3 * (1 - t) ** 2 * t * p_1 + 3 * (1 - t) * t ** 2 * p_2 + t ** 3 * p_3) for t in t_arr]


def task_a():
    a = [100, 100]
    k_1 = 2
    phi = np.pi / 4
    k_2 = 1 / 2

    new_color = (200, 0, 200)
    base = np.array([[-200, -100, 1], [100, 400, 1], [450, -200, 1]])
    draw_axis()

    arr = get_bezier_curve_2(base)
    draw(arr)

    # arr = affine.Ta(a, arr)
    # arr = affine.Shx(k_1, arr)
    # arr = affine.Ro(phi, arr)
    # arr = affine.Ho(k_2, arr)
    # draw(arr, new_color)

    arr = get_bezier_curve_2(base)
    transform_matrix = np.array([
        [k_2 * np.cos(phi), k_2 * np.sin(phi) + k_1 * k_2 * np.cos(phi),    a[0] * k_2 * np.cos(phi) + a[1] * (k_2 * np.sin(phi) + k_1 * k_2 * np.cos(phi))],
        [k_2 * (-np.sin(phi)), k_2 * np.cos(phi) - k_1 * k_2 * np.sin(phi), a[1] * (k_2 * np.cos(phi) - k_1 * k_2 * np.sin(phi)) - a[0] * k_2 * np.sin(phi)],
        [0, 0, 1]
    ])
    arr = affine.transform(transform_matrix, arr)
    draw(arr, new_color)

    img.show()


def task_b():
    draw_axis()

    base = np.array([[0, 0, 1], [0, 400, 1], [400, 400, 1], [400, 0, 1]])
    arr = get_bezier_curve_3(base)
    arr = affine.Ta([50, 50], arr)
    draw(arr)

    base = np.array([[0, 0, 1], [100, 400, 1], [300, 400, 1], [400, 0, 1]])
    arr = get_bezier_curve_3(base)
    arr = affine.Ta([-450, 50], arr)
    draw(arr)

    base = np.array([[0, 0, 1], [400, 400, 1], [0, 400, 1], [400, 0, 1]])
    arr = get_bezier_curve_3(base)
    arr = affine.Ta([-450, -450], arr)
    draw(arr)

    base = np.array([[0, 0, 1], [100, 400, 1], [300, 0, 1], [400, 400, 1]])
    arr = get_bezier_curve_3(base)
    arr = affine.Ta([50, -450], arr)
    draw(arr)

    img.show()


def task_c():
    base = np.array([[-100, 200, 1], [0, 600, 1], [100, 200, 1]])
    arr = get_bezier_curve_2(base)
    draw(arr)

    base = np.array([[100, 200, 1], [200, -200, 1], [300, 200, 1], [400, -200, 1]])
    arr = get_bezier_curve_3(base)
    draw(arr)

    base = np.array([[400, -200, 1], [450, -400, 1], [-450, -400, 1], [-400, -200, 1]])
    arr = get_bezier_curve_3(base)
    draw(arr)

    base = np.array([[-400, -200, 1], [-300, 200, 1], [-200, -200, 1], [-100, 200, 1]])
    arr = get_bezier_curve_3(base)
    draw(arr)

    img.show()

task_c()
