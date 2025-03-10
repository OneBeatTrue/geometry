import numpy as np
import matplotlib.pyplot as plt

c = 3

ts = np.linspace(0, 2 * np.pi, 1000)

x_fun = lambda t: c * np.sqrt(2) * np.cos(t) / (1 + np.sin(t) ** 2)
y_fun = lambda t: c * np.sqrt(2) * np.sin(t) * np.cos(t) / (1 + np.sin(t) ** 2)
x = x_fun(ts)
y = y_fun(ts)

plt.plot(x, y, marker=None, linestyle='-', color='blue')
plt.axis('equal')
plt.grid(True)


t_0 = np.pi / 6
x_0 = x_fun(t_0)
y_0 = y_fun(t_0)

tangent = lambda t: (6 * np.sin(t) - 2 / np.sin(t)) / (np.cos(2 * t) + 5)
tan_fun = lambda x, t: tangent(t) * (x - x_0) + y_0
norm_fun = lambda x, t: -1 / tangent(t) * (x - x_0) + y_0
x = [x_0 - 1, x_0 + 1]
plt.plot(x, [tan_fun(x[0], t_0), tan_fun(x[1], t_0)] , marker=None, linestyle='-', color='black', linewidth=1)
plt.plot(x, [norm_fun(x[0], t_0), norm_fun(x[1], t_0)] , marker=None, linestyle='-', color='black', linewidth=1)
plt.ylim(min(y) - 1, max(y) + 1)

K_fun = lambda t: ((24 * c ** 2 * np.abs(np.cos(t)) / (np.cos(2 * t) - 3) ** 2) /
                   (8 * c ** 2 * np.cos(t) ** 2 * (np.cos(2 * t) - 19) / (np.cos(2 * t) - 3) ** 3) ** 1.5)
K = K_fun(t_0)
print("Radius:")
print(1 / K)
plt.show()
