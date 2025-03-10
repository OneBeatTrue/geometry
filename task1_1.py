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



def last(k, arr):
    mid = (arr[0] + arr[1]) / 2
    arr = affine.Ta(-mid[:2], arr)
    arr = affine.Ho(k, arr)
    arr = affine.Ro(np.pi, arr)
    arr = affine.Ta(mid[:2], arr)
    return arr


arr = np.array([
    [1, 1, 1],
    [0.7, 3, 1],
    [2, 1, 1]
])

a = np.array([2, 3])
phi = np.pi / 2
k = 2

draw(arr)
draw(affine.Ta(a, arr))
draw(affine.Ro(phi, arr))
draw(affine.Sy(arr))
draw(affine.Ho(k, arr))

draw(last(3, arr))

plt.show()