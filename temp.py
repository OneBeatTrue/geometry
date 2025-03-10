import numpy as np
import matplotlib.pyplot as plt


xa, ya = -10, -7
xb, yb = 15, 23

plt.plot([xa, xb], [ya, yb], marker=None, linestyle='-', color='red')
plt.vlines(x=0, ymin=ya, ymax=yb)
plt.hlines(y=0, xmin=xa, xmax=xb)
plt.axis('equal')
plt.grid(True)

plt.show()
