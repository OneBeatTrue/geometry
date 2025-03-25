import numpy as np
import matplotlib.pyplot as plt

c = 0.5

ts = np.linspace(0, 4 * np.pi, 1000)

x_fun = lambda t: c * t * np.cos(t)
y_fun = lambda t: c * t * np.sin(t)
x = x_fun(ts)
y = y_fun(ts)

plt.plot(x, y, marker=None, linestyle='-', color='blue')
plt.axis('equal')
plt.grid(True)


t_0 = 8 * np.pi / 4
x_0 = x_fun(t_0)
y_0 = y_fun(t_0)

tangent = lambda t: (np.sin(t) + t * np.cos(t)) / (np.cos(t) - t * np.sin(t))
tan_fun = lambda x, t: tangent(t) * (x - x_0) + y_0
norm_fun = lambda x, t: -1 / tangent(t) * (x - x_0) + y_0
x = [x_0 - 1, x_0 + 1]
plt.plot(x, [tan_fun(x[0], t_0), tan_fun(x[1], t_0)] , marker=None, linestyle='-', color='black', linewidth=1)
plt.plot(x, [norm_fun(x[0], t_0), norm_fun(x[1], t_0)] , marker=None, linestyle='-', color='black', linewidth=1)
plt.ylim(min(y) - 1, max(y) + 1)

K_fun = lambda t: c ** 2 * (t ** 2 + 2) / (c ** 2 * (t ** 2 + 4)) ** 1.5
K = K_fun(t_0)
print("Radius:")
print(1 / K)
plt.show()
