import numpy as np
import matplotlib.pyplot as plt
from affine import Affine

affine = Affine()


def draw(nparr):
    arr = np.vstack([nparr, nparr[0]])
    x, y = arr[:, 0], arr[:, 1]

    plt.plot(x, y, marker='.', linestyle='-')
    plt.axis('equal')
    plt.grid(True)

l = 4
arr = np.array([
    [0, 0, 1],
    [0, l, 1],
    [l, l, 1],
    [l, 0, 1],
])

a = 3 * (arr[2] - arr[0])
sheer = 1 / np.tan(np.pi / 3)
k = 2

draw(arr)
print("Original square:")
print(arr)
print()

matrix = np.array([
    [k, sheer * k, a[0]],
    [0, k, a[1]],
    [0, 0, 1],
])
print("Transform matrix:")
print(matrix)
print()

arr = affine.transform(matrix, arr)
draw(arr)
print("Transformed square:")
print(arr)
print()

inv_matrix = np.linalg.inv(matrix)
print("Inverted transform matrix:")
print(inv_matrix)
print()

arr = affine.transform(inv_matrix, arr)
draw(arr)
print("Back transformed square:")
print(np.round(arr, 8))
print()

plt.show()