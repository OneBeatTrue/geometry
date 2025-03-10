import numpy as np
import matplotlib.pyplot as plt

a = 2
b = 3

alpha_fun = lambda t: np.cos(t) * (a - (a ** 2 * np.sin(t) ** 2 + b ** 2 * np.cos(t) ** 2) / a)
beta_fun = lambda t: np.sin(t) * (b - (a ** 2 * np.sin(t) ** 2 + b ** 2 * np.cos(t) ** 2) / b)

ts = np.linspace(0, 2 * np.pi, 1000)

x, y = a * np.cos(ts), b * np.sin(ts)

plt.plot(x, y, marker=None, linestyle='-', color='blue')
plt.axis('equal')
plt.grid(True)

t_n = np.linspace(0, 2 * np.pi, 100)
x = np.array([-3, 3])
tangent = lambda x, t: -b / a / np.tan(t) * (x - a * np.cos(t)) + b * np.sin(t)
for i in range(1, len(t_n)):
    t = (t_n[i - 1] + t_n[i]) / 2
    plt.plot(x, [tangent(x[0], t), tangent(x[1], t)] , marker=None, linestyle='-', color='black', linewidth=1)



x, y = alpha_fun(ts), beta_fun(ts)

plt.plot(x, y, marker=None, linestyle='-', color='red')
plt.axis('equal')
plt.ylim(-4, 4)
plt.grid(True)

plt.show()
